"""initial_schema

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-10-07 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '0001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('username', sa.String(length=64), nullable=False),
        sa.Column('email', sa.String(length=128), nullable=False),
        sa.Column('password_hash', sa.String(length=256), nullable=False),
        sa.Column('role', sa.String(length=32), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # Documents table
    op.create_table(
        'documents',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('external_ref', sa.String(length=64), nullable=False),
        sa.Column('doc_type', sa.String(length=32), nullable=False),
        sa.Column('raw_text_encrypted', sa.LargeBinary(), nullable=True),
        sa.Column('deid_text', sa.Text(), nullable=False),
        sa.Column('phi_map_encrypted', sa.LargeBinary(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False),
        sa.Column('ocr_applied', sa.Boolean(), nullable=False),
        sa.Column('ocr_low_confidence_count', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_documents_created_at'), 'documents', ['created_at'], unique=False)
    op.create_index(op.f('ix_documents_external_ref'), 'documents', ['external_ref'], unique=False)
    op.create_index(op.f('ix_documents_status'), 'documents', ['status'], unique=False)

    # Pipeline Runs table
    op.create_table(
        'pipeline_runs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('document_id', sa.UUID(), nullable=False),
        sa.Column('stage', sa.String(length=32), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('model_versions', sa.JSON(), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('finished_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('error', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Entities table
    op.create_table(
        'entities',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('document_id', sa.UUID(), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('label', sa.String(length=32), nullable=False),
        sa.Column('start_char', sa.Integer(), nullable=False),
        sa.Column('end_char', sa.Integer(), nullable=False),
        sa.Column('section', sa.String(length=64), nullable=False),
        sa.Column('assertion', sa.String(length=32), nullable=False),
        sa.Column('concept_id', sa.String(length=32), nullable=True),
        sa.Column('ner_conf', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_entities_document_id'), 'entities', ['document_id'], unique=False)

    # ICD10 Codes table
    op.create_table(
        'icd10_codes',
        sa.Column('code', sa.String(length=16), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('chapter', sa.String(length=128), nullable=True),
        sa.Column('block', sa.String(length=128), nullable=True),
        sa.Column('category', sa.String(length=64), nullable=True),
        sa.Column('billable', sa.Boolean(), nullable=False),
        sa.Column('excludes1', sa.JSON(), nullable=True),
        sa.Column('synonyms', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('code')
    )

    # Code Suggestions table
    op.create_table(
        'code_suggestions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('document_id', sa.UUID(), nullable=False),
        sa.Column('entity_id', sa.UUID(), nullable=False),
        sa.Column('icd10_code', sa.String(length=16), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('rank', sa.SmallInteger(), nullable=False),
        sa.Column('raw_score', sa.Float(), nullable=False),
        sa.Column('calibrated_conf', sa.Float(), nullable=False),
        sa.Column('band', sa.String(length=16), nullable=False),
        sa.Column('justification_md', sa.Text(), nullable=True),
        sa.Column('grounded', sa.Boolean(), nullable=True),
        sa.Column('evidence_spans', sa.JSON(), nullable=True),
        sa.Column('provenance', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['entity_id'], ['entities.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['icd10_code'], ['icd10_codes.code']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_code_suggestions_band'), 'code_suggestions', ['band'], unique=False)
    op.create_index(op.f('ix_code_suggestions_document_id'), 'code_suggestions', ['document_id'], unique=False)
    op.create_index(op.f('ix_code_suggestions_icd10_code'), 'code_suggestions', ['icd10_code'], unique=False)

    # Review Actions table
    op.create_table(
        'review_actions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('suggestion_id', sa.UUID(), nullable=False),
        sa.Column('coder_id', sa.UUID(), nullable=False),
        sa.Column('action', sa.String(length=16), nullable=False),
        sa.Column('final_code', sa.String(length=16), nullable=True),
        sa.Column('reason', sa.String(length=128), nullable=True),
        sa.Column('at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['coder_id'], ['users.id']),
        sa.ForeignKeyConstraint(['suggestion_id'], ['code_suggestions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Chart Submissions table
    op.create_table(
        'chart_submissions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('document_id', sa.UUID(), nullable=False),
        sa.Column('coder_id', sa.UUID(), nullable=False),
        sa.Column('final_codes', sa.JSON(), nullable=False),
        sa.Column('qa_pair_id', sa.UUID(), nullable=True),
        sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['coder_id'], ['users.id']),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # CDI Queries table
    op.create_table(
        'cdi_queries',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('document_id', sa.UUID(), nullable=False),
        sa.Column('gap_type', sa.String(length=64), nullable=False),
        sa.Column('query_md', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Audit Log table
    op.create_table(
        'audit_log',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('ts', sa.DateTime(timezone=True), nullable=False),
        sa.Column('actor', sa.String(length=128), nullable=False),
        sa.Column('action', sa.String(length=64), nullable=False),
        sa.Column('resource_type', sa.String(length=64), nullable=False),
        sa.Column('resource_id', sa.String(length=128), nullable=False),
        sa.Column('detail', sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Investigation Runs table
    op.create_table(
        'investigation_runs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('document_id', sa.UUID(), nullable=False),
        sa.Column('trigger', sa.String(length=32), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('report', sa.JSON(), nullable=True),
        sa.Column('agent_versions', sa.JSON(), nullable=True),
        sa.Column('verifier_pass', sa.Boolean(), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('finished_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('investigation_runs')
    op.drop_table('audit_log')
    op.drop_table('cdi_queries')
    op.drop_table('chart_submissions')
    op.drop_table('review_actions')
    op.drop_table('code_suggestions')
    op.drop_table('icd10_codes')
    op.drop_table('entities')
    op.drop_table('pipeline_runs')
    op.drop_table('documents')
    op.drop_table('users')
