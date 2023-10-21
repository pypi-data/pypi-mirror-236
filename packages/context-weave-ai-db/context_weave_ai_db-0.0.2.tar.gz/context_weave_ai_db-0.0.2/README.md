# Context Weave AI DB package

This repo hosts the source code for the db package for [Context Weave AI](https://contextweave.ai/).

## Setup dev environment

1. Create virtual environment: `conda create -n context-weave-db-env -y python=3.10`
1. Activate virtual environment: `conda activate context-weave-db-env`
1. Install dependencies: `pip install --upgrade -r requirements.txt`

## DB migration changes using alembic

Setting up Alembic in an existing application that uses SQLAlchemy involves a series of steps. Alembic is a database migration tool that works well with SQLAlchemy to manage changes to the database schema over time. Here's a step-by-step guide:

1. **Install Alembic:**
   Install Alembic using pip:

   ```bash
   pip install alembic
   ```

2. **Create Alembic Configuration:**
   Create an Alembic configuration file, typically named `alembic.ini`. You can generate a basic configuration file using the following command:

   ```bash
   alembic init alembic
   ```

   This command creates an `alembic` directory with configuration files and folders.

3. **Configure Alembic:**
   Edit the `alembic.ini` file to set the correct database URL. Update the `sqlalchemy.url` configuration to match your PostgreSQL connection details.

   ```ini
   # alembic.ini

   sqlalchemy.url = postgresql://user:password@localhost:5432/database
   ```

4. **Configure Alembic Environment:**
   Edit the `alembic/env.py` file to include the SQLAlchemy model and the target metadata.

   ```python
   # alembic/env.py
   from myapp.models import Base  # Import your SQLAlchemy Base

   target_metadata = Base.metadata
   ```

   Replace `myapp.models` with the correct path to your SQLAlchemy models.

5. **Create Initial Migration:**
   Generate an initial migration to capture the existing database schema:

   ```bash
   alembic revision --autogenerate -m "initial"
   ```

   This creates a new migration script in the `alembic/versions` directory.

6. **Review and Apply Initial Migration:**
   Review the generated migration script in the `alembic/versions` directory. If everything looks correct, apply the initial migration to the database:

   ```bash
   alembic upgrade head
   ```

7. **Make Model Changes:**
   Update your SQLAlchemy models to reflect the desired changes in your application. For example, add or modify columns.

8. **Generate a Migration Script:**
   Generate a new migration script for the changes:

   ```bash
   alembic revision --autogenerate -m "description_of_changes"
   ```

   This generates a new migration script in the `alembic/versions` directory based on the changes made to the SQLAlchemy models.

9. **Review and Apply the Migration:**
   Review the generated migration script, and if everything looks correct, apply the migration to the database:

   ```bash
   alembic upgrade head
   ```

   This updates the database schema to reflect the changes made to the SQLAlchemy models.

10. **Repeat for Future Changes:**
    Repeat steps 7-9 for any future changes to the database schema.

By following these steps, you can set up Alembic in your existing application that uses SQLAlchemy, and you can use Alembic to manage database migrations as your application evolves.
