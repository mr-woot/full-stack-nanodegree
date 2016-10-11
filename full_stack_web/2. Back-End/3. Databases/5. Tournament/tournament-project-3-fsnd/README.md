# Tournament Project-Full Stack Nanodegree

## Steps to Run on Linux/Windows:
- ``git clone https://github.com/mr-woot/tournament-project-3-fsnd.git``.
- Go into the cloned repository on Desktop.
- Make sure, vagrant is installed on your system with proper OS compatible version.
- Open terminal from the repo directory:
  - Type``cd /vagrant``
  - Then type ``vagrant up``, wait for the setup to finish.
  - Then ``vagrant ssh``.
  - After login to vagrant, type ``psql``, then enter.
  - Connect to tournament database using ``\c tournament``.
  - To check the Unit Tests, run ``python tournament_test.py``.
- To know about table definition, type ``\dt`` in psql terminal. 
