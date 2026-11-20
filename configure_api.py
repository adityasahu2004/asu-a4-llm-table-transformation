"""Run locally in Terminal; never paste a key into chat or command history."""
from getpass import getpass
import os
from pathlib import Path

if __name__ == '__main__':
    key=getpass('Paste ASU API key (hidden): ').strip()
    if not key or '\n' in key:
        raise SystemExit('Invalid key')
    path=Path(__file__).with_name('.env')
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600)
    os.fchmod(fd,0o600)
    with os.fdopen(fd,'w') as stream:
        stream.write('OPENAI_API_KEY='+key+'\nOPENAI_BASE_URL=https://openai.rc.asu.edu/v1\n')
    print('Saved locally. The submission packager excludes this file.')
