from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'job_postings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('company', sa.String(200), nullable=False),
        sa.Column('location', sa.String(200)),
        sa.Column('description', sa.Text),
        sa.Column('salary_range', sa.String(200)),
        sa.Column('link', sa.String(500), unique=True),
        sa.Column('platform', sa.String(50)),
        sa.Column('posted_date', sa.DateTime),
        sa.Column('created_at', sa.DateTime),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_job_postings_link', 'job_postings', ['link'], unique=True)
    op.create_index('ix_job_postings_platform', 'job_postings', ['platform'])
    op.create_index('ix_job_postings_posted_date', 'job_postings', ['posted_date'])

def downgrade():
    op.drop_table('job_postings')