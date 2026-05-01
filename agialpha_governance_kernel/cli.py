import argparse
from .kernel import GovernanceKernel

def main():
    p=argparse.ArgumentParser()
    p.add_argument("kernel")
    a=p.parse_args()
    k=GovernanceKernel.load(a.kernel)
    print({"human_review_required":k.require_human_review()})

if __name__=="__main__":
    main()
