from pathlib import Path

def export_opa(kernel_path, out_dir):
    o=Path(out_dir); o.mkdir(parents=True, exist_ok=True)
    (o/"README.md").write_text("Optional OPA/Rego export only. Runtime OPA is not required.\n")
    (o/"policy.rego").write_text("package securerails\n# static interoperability example\ndefault decision = \"escalate\"\n")
