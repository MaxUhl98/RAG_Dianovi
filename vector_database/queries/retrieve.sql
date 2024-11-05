SELECT document_filename, document_title, section_title, headings, text_content, is_table ,page_number, abs(1 - (embedding <=> '{}')) AS cosine_similarity from rag_test
where length(text_content) > 30 and section_title not like '%Literatur%' and text_content not like '%Nein: 0%' and not is_table
order by cosine_similarity desc
limit {}