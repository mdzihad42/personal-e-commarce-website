Upgrade to Python 3.13 — notes

What I did (automated by Copilot):

1. Verified Python 3.13 is available (`py -3.13 -V` → 3.13.11).
2. Created a new virtual environment `env3.13`:
   ```powershell
   py -3.13 -m venv env3.13
   ```
3. Upgraded pip tools and installed dependencies:
   ```powershell
   .\env3.13\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
   .\env3.13\Scripts\python.exe -m pip install -r ecommarce\requirements.txt
   ```
4. Verified Django checks and tests:
   ```powershell
   ..\env3.13\Scripts\python.exe manage.py check
   ..\env3.13\Scripts\python.exe manage.py test
   ```

Notes & recommendations:
- No compatibility issues were found with the packages in `requirements.txt` for Python 3.13.11 in this environment.
- Add real unit tests to the project so future upgrades are safer.
- Keep `env3.13/` out of version control (already added to `.gitignore`).

If you want, I can remove `env/` now (your old venv) or leave both; I recommend keeping only `env3.13` going forward and deleting the old virtualenv if not needed.