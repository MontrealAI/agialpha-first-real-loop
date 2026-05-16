import subprocess, sys, tempfile

def test_customer_mode_not_reported_rejected():
    d = tempfile.mkdtemp()
    proc = subprocess.run([
        sys.executable, '-m', 'agialpha_enterprise_pilot', 'build',
        '--repo-root', '.', '--out', d,
        '--workflow-family', 'software_quality_pack',
        '--customer-mode', 'not_reported'
    ], capture_output=True, text=True)
    assert proc.returncode != 0
