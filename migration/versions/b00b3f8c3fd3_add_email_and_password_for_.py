from alembic import op
import sqlalchemy as sa


revision = 'b00b3f8c3fd3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # 1. Create new table with correct schema
    op.create_table(
        'users_new',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
    )

    # 2. Copy & transform old data
    # Note: If existing rows had NULL email/password, you must fill something
    op.execute("""
        INSERT INTO users_new (id, email, password)
        SELECT 
            id,
            email,
            password
        FROM users;
    """)

    # 3. Drop old table
    op.drop_table('users')

    # 4. Rename new table into place
    op.rename_table('users_new', 'users')


def downgrade():
    # Rebuild original structure
    op.create_table(
        'users_old',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('fullName', sa.String(), nullable=False),
        sa.Column('phoneNumber', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('password', sa.String(), nullable=True),
    )

    op.execute("""
        INSERT INTO users_old (id, fullName, phoneNumber, email, password)
        SELECT
            id,
            fullName,
            phoneNumber,
            email,
            password
        FROM users;
    """)

    op.drop_table('users')
    op.rename_table('users_old', 'users')
