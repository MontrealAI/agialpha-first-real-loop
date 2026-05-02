from .global_generator import generate_opportunities

def detect_opportunity_gradients(count:int,start_index:int=0):
    return generate_opportunities(count,start_index=start_index)
