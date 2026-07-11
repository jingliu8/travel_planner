create or replace function match_documents(
    query_embedding vector(1536),
    match_count int
)
returns table (
    id text,
    source text,
    content text,
    similarity float
)
language sql
as $$
    select
        id,
        source,
        content,
        1 - (embedding <=> query_embedding) as similarity
    from documents
    order by embedding <=> query_embedding
    limit match_count;
$$;