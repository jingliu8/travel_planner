from unittest.mock import Mock

from llm import LLMClient

def test_llm_generate():

    # Mock OpenAI response
    mock_response = Mock()
    mock_response.output_text = "A 4-day Asheville itinerary"

    # Mock OpenAI client
    mock_client = Mock()
    mock_client.responses.create.return_value = mock_response

    # Create LLM client with mocked OpenAI client
    llm = LLMClient(client=mock_client)

    result = llm.generate(
        system_prompt="You are a travel planner.",
        user_input="Plan a trip to Asheville."
    )

    # Verify output
    assert result == "A 4-day Asheville itinerary"

    # Verify OpenAI API was called correctly
    mock_client.responses.create.assert_called_once_with(
        model=llm.model,
        instructions="You are a travel planner.",
        input="Plan a trip to Asheville."
    )