-- =====================================================
-- AIRR Transcript Parser - Learn-as-you-go Schema
-- =====================================================
-- No predefined templates - system learns from successful parses
-- =====================================================

-- Table: Learned Templates (auto-populated)
CREATE TABLE IF NOT EXISTS learned_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- University identification (learned from transcripts)
    university_name TEXT NOT NULL,
    university_aliases TEXT[] DEFAULT '{}',
    
    -- Layout characteristics (detected by agent)
    layout_type TEXT,  -- 'tabular', 'semester-block', 'multi-column', etc.
    layout_fingerprint JSONB NOT NULL,  -- structural features for matching
    /*
      Example:
      {
        "header_position": "top-center",
        "has_logo": true,
        "grade_format": "letter",  -- "letter", "10-point", "percentage"
        "semester_organization": "vertical-blocks",
        "table_structure": "single-table" | "multi-table",
        "key_fields_detected": ["student_name", "roll_number", "cgpa"]
      }
    */
    
    -- The generated parsing prompt that worked
    parsing_prompt TEXT NOT NULL,
    
    -- Output schema that was successfully extracted
    output_schema JSONB,
    
    -- Learning metrics
    times_used INT DEFAULT 1,
    success_count INT DEFAULT 1,
    last_used_at TIMESTAMPTZ DEFAULT now(),
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,  -- manually verified as accurate
    
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    
    -- Prevent exact duplicates
    UNIQUE(university_name, layout_type)
);

-- Table: Parse History (all attempts)
CREATE TABLE IF NOT EXISTS parse_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- What was detected
    detected_university TEXT,
    detected_layout_type TEXT,
    layout_analysis JSONB,  -- full analysis from first agent
    
    -- Which template was used (null if dynamic)
    template_id UUID REFERENCES learned_templates(id),
    used_learned_template BOOLEAN DEFAULT false,
    
    -- The prompt that was used
    prompt_used TEXT,
    
    -- Results
    raw_output JSONB,
    parsed_successfully BOOLEAN,
    validation_errors TEXT[],
    
    -- Should we learn from this?
    eligible_for_learning BOOLEAN DEFAULT false,
    was_saved_as_template BOOLEAN DEFAULT false,
    
    -- Metadata
    processing_time_ms INT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- =====================================================
-- Indexes
-- =====================================================
CREATE INDEX IF NOT EXISTS idx_templates_university ON learned_templates(university_name);
CREATE INDEX IF NOT EXISTS idx_templates_active ON learned_templates(is_active) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_templates_usage ON learned_templates(times_used DESC);
CREATE INDEX IF NOT EXISTS idx_history_created ON parse_history(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_history_success ON parse_history(parsed_successfully);

-- Full text search on university name
CREATE INDEX IF NOT EXISTS idx_templates_university_search 
ON learned_templates USING gin(to_tsvector('english', university_name));

-- =====================================================
-- Updated_at Trigger
-- =====================================================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS templates_updated_at ON learned_templates;
CREATE TRIGGER templates_updated_at
    BEFORE UPDATE ON learned_templates
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- =====================================================
-- Function: Find matching template
-- =====================================================
CREATE OR REPLACE FUNCTION find_matching_template(
    p_university TEXT,
    p_layout_type TEXT DEFAULT NULL
)
RETURNS TABLE (
    id UUID,
    university_name TEXT,
    layout_type TEXT,
    parsing_prompt TEXT,
    match_score INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        lt.id,
        lt.university_name,
        lt.layout_type,
        lt.parsing_prompt,
        (
            -- Exact name match
            CASE WHEN LOWER(lt.university_name) = LOWER(p_university) THEN 100
            -- Partial match
            WHEN LOWER(lt.university_name) LIKE '%' || LOWER(p_university) || '%' THEN 70
            WHEN LOWER(p_university) LIKE '%' || LOWER(lt.university_name) || '%' THEN 70
            -- Alias match
            WHEN EXISTS (
                SELECT 1 FROM unnest(lt.university_aliases) alias 
                WHERE LOWER(alias) = LOWER(p_university)
            ) THEN 90
            WHEN EXISTS (
                SELECT 1 FROM unnest(lt.university_aliases) alias 
                WHERE LOWER(alias) LIKE '%' || LOWER(p_university) || '%'
            ) THEN 60
            ELSE 0
            END
            +
            -- Layout type bonus
            CASE WHEN p_layout_type IS NOT NULL AND lt.layout_type = p_layout_type THEN 20 ELSE 0 END
            +
            -- Usage bonus (more used = more reliable)
            LEAST(lt.times_used, 10)
            +
            -- Verified bonus
            CASE WHEN lt.is_verified THEN 15 ELSE 0 END
        )::INT as match_score
    FROM learned_templates lt
    WHERE lt.is_active = true
    ORDER BY match_score DESC
    LIMIT 5;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- Function: Update template usage stats
-- =====================================================
CREATE OR REPLACE FUNCTION increment_template_usage(
    p_template_id UUID,
    p_was_successful BOOLEAN
)
RETURNS VOID AS $$
BEGIN
    UPDATE learned_templates
    SET 
        times_used = times_used + 1,
        success_count = success_count + CASE WHEN p_was_successful THEN 1 ELSE 0 END,
        last_used_at = now()
    WHERE id = p_template_id;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- Row Level Security
-- =====================================================
ALTER TABLE learned_templates ENABLE ROW LEVEL SECURITY;
ALTER TABLE parse_history ENABLE ROW LEVEL SECURITY;

-- Service role full access
CREATE POLICY "Service role full access on templates"
    ON learned_templates FOR ALL
    USING (auth.role() = 'service_role');

CREATE POLICY "Service role full access on history"
    ON parse_history FOR ALL
    USING (auth.role() = 'service_role');

-- Anon read-only for active templates
CREATE POLICY "Anon read active templates"
    ON learned_templates FOR SELECT
    USING (is_active = true);

-- =====================================================
-- Helpful Views
-- =====================================================

-- View: Template performance
CREATE OR REPLACE VIEW template_performance AS
SELECT 
    id,
    university_name,
    layout_type,
    times_used,
    success_count,
    ROUND(100.0 * success_count / NULLIF(times_used, 0), 1) as success_rate,
    is_verified,
    last_used_at,
    created_at
FROM learned_templates
WHERE is_active = true
ORDER BY times_used DESC;

-- View: Recent parse attempts
CREATE OR REPLACE VIEW recent_parses AS
SELECT 
    id,
    detected_university,
    detected_layout_type,
    used_learned_template,
    parsed_successfully,
    was_saved_as_template,
    created_at
FROM parse_history
ORDER BY created_at DESC
LIMIT 100;

ALTER TABLE parse_history 
ADD COLUMN IF NOT EXISTS input_image_base64 TEXT,
ADD COLUMN IF NOT EXISTS output_json JSONB;
-- =====================================================
-- Done! Schema ready for learn-as-you-go system.
-- =====================================================