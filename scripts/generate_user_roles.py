import argparse
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_user_roles, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    users = gen_user_roles()
    write_jsonl("data/instana/user_roles.jsonl", [users])

if __name__ == "__main__":
    main()
