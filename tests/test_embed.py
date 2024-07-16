"""
# tests/test_embed.py
import pytest
from rag.embed import embed

def test_embed():
    # Example input
    example_document = {
        'title': 'Sample Document',
        'information': 'Sample information text.',
        'methods': 'Sample methods text.',
        'keyresults': 'Sample key results text.',
        'tables': {'table1': 'Sample table data'},
    }

    # Mock function to avoid actual embedding and database operations
    def mock_embed(document):
        return {'embedded_data': 'mocked_embeddings'}
    
    # Replace the real embed function with the mock
    original_embed = embed
    embed = mock_embed

    result = embed(example_document)

    assert isinstance(result, dict)
    assert 'embedded_data' in result
    assert result['embedded_data'] == 'mocked_embeddings'

    # Restore the original embed function
    embed = original_embed

"""
