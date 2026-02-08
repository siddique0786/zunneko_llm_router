from src.router.intelligent_router import IntelligentRouter
import uuid
from src.metrics.store import track_cost, calculate_cost

router = IntelligentRouter()


def process_llm_request(prompt: str):

    request_id = str(uuid.uuid4())

    print(f"Processing request {request_id}")

    # ⭐ Router now returns response + provider name
    response, provider_name = router.route(prompt)

    # ----- TOKEN ESTIMATION -----
    input_tokens = len(prompt.split())
    output_tokens = len(response.split())

    # ----- COST CALCULATION -----
    cost = calculate_cost(
        provider_name,
        input_tokens,
        output_tokens
    )

    track_cost(
        provider_name,
        input_tokens + output_tokens,
        cost
    )

    print(f"[Cost] Provider: {provider_name}")
    print(f"[Cost] Tokens Used: {input_tokens + output_tokens}")
    print(f"[Cost] Estimated Cost: ${cost:.6f}")

    return {
        "request_id": request_id,
        "response": response
    }






# from src.router.intelligent_router import IntelligentRouter
# import uuid
# # from src.metrics.store import track_cost, calculate_cost


# router = IntelligentRouter()


# def process_llm_request(prompt: str):

#     request_id = str(uuid.uuid4())

#     print(f"Processing request {request_id}")

#     response = router.route(prompt)

#     return {
#         "request_id": request_id,
#         "response": response
#     }




# import time
# import uuid


# def process_llm_request(prompt: str):
#     request_id = str(uuid.uuid4())

#     print(f"Processing request {request_id}")

#     # Simulate processing delay
#     time.sleep(2)

#     return {
#         "request_id": request_id,
#         "response": f"Processed prompt: {prompt}"
#     }
