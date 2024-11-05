create table rag_test
(
    id                SERIAL PRIMARY KEY,
    document_title    varchar(255),
    section_title     varchar(1000),
    headings          varchar(255),
    embedded_text     text,
    embedding         vector(1024),
    text_content      text,
    is_table          boolean,
    document_filename varchar(255),
    page_number       integer,
    created_at        timestamp default NOW(),
    updated_at        timestamp default NOW()
);

CREATE OR REPLACE FUNCTION update_timestamp()
    RETURNS TRIGGER AS
$$
BEGIN
    -- Check if any column values have changed
    IF NEW.* IS DISTINCT FROM OLD.* THEN
        NEW.updated_at = NOW(); -- Update the timestamp only if values have changed
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_timestamp
    BEFORE UPDATE
    ON rag_test
    FOR EACH ROW
EXECUTE FUNCTION update_timestamp();


