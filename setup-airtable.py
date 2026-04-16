#!/usr/bin/env python3
"""
Sun Holdings — Airtable Base Setup Script
Run this once to create all required tables in your new Airtable base.

Usage:
  1. Get your Airtable Personal Access Token from:
     https://airtable.com/create/tokens
     (Needs scopes: data.records:write, schema.bases:write)
  2. Set BASE_ID and TOKEN below
  3. Run: python3 setup-airtable.py
"""

import json, urllib.request, urllib.error

BASE_ID = 'appFF43iOykm30NYL'
TOKEN   = 'YOUR_AIRTABLE_TOKEN_HERE'   # ← paste your token

API = f'https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables'
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

def create_table(name, description, fields):
    body = json.dumps({'name': name, 'description': description, 'fields': fields}).encode()
    req = urllib.request.Request(API, data=body, headers=HEADERS, method='POST')
    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read())
            print(f'  ✓ Created table: {name}  (id: {data["id"]})')
            return data
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f'  ✗ Failed to create {name}: {e.code} {err}')
        return None

print(f'\nSetting up Airtable base {BASE_ID}...\n')

# ── Users ────────────────────────────────────────────────────────────────────
create_table('Users', 'Portal users (attorneys and staff)', [
    {'name': 'Name',       'type': 'singleLineText'},
    {'name': 'Email',      'type': 'email'},
    {'name': 'Department', 'type': 'singleSelect', 'options': {'choices': [
        {'name': 'Legal'}, {'name': 'Finance'}, {'name': 'Operations'}, {'name': 'HR'}]}},
    {'name': 'Phone',      'type': 'phoneNumber'},
    {'name': 'Role',       'type': 'singleSelect', 'options': {'choices': [
        {'name': 'admin'}, {'name': 'attorney'}, {'name': 'staff'}]}},
    {'name': 'PIN',        'type': 'singleLineText'},
])

# ── Tickets ──────────────────────────────────────────────────────────────────
create_table('Tickets', 'Legal request tickets', [
    {'name': 'Title',           'type': 'multilineText'},
    {'name': 'Submitter Name',  'type': 'singleLineText'},
    {'name': 'Description',     'type': 'multilineText'},
    {'name': 'Department',      'type': 'singleSelect', 'options': {'choices': [
        {'name': 'Legal'}, {'name': 'Finance'}, {'name': 'Operations'},
        {'name': 'HR'}, {'name': 'Executive'}]}},
    {'name': 'Category',        'type': 'singleSelect', 'options': {'choices': [
        {'name': 'Contract Review'}, {'name': 'Corporate'}, {'name': 'Employment'},
        {'name': 'Compliance'}, {'name': 'Litigation'}, {'name': 'General'}]}},
    {'name': 'Status',          'type': 'singleSelect', 'options': {'choices': [
        {'name': 'New'}, {'name': 'In Progress'}, {'name': 'Urgent'},
        {'name': 'On Hold'}, {'name': 'Completed'}]}},
    {'name': 'Priority',        'type': 'singleSelect', 'options': {'choices': [
        {'name': 'Low'}, {'name': 'Medium'}, {'name': 'High'}, {'name': 'Critical'}]}},
    {'name': 'Counterparty',    'type': 'singleLineText'},
    {'name': 'Assigned To',     'type': 'singleLineText'},
    {'name': 'Deadline',        'type': 'date', 'options': {'dateFormat': {'name': 'us'}}},
    {'name': 'Submitter Email', 'type': 'email'},
    {'name': 'Attorney Email',  'type': 'email'},
    {'name': 'Confidentiality', 'type': 'multilineText'},
])

# ── Messages ─────────────────────────────────────────────────────────────────
create_table('Messages', 'Ticket thread messages', [
    {'name': 'Sender Name', 'type': 'singleLineText'},
    {'name': 'Sender Role', 'type': 'singleSelect', 'options': {'choices': [
        {'name': 'admin'}, {'name': 'attorney'}, {'name': 'staff'}, {'name': 'submitter'}]}},
    {'name': 'Body',            'type': 'multilineText'},
    {'name': 'Recipient Email', 'type': 'email'},
])

# ── Documents ────────────────────────────────────────────────────────────────
create_table('Documents', 'Uploaded documents and generated files', [
    {'name': 'Filename',      'type': 'singleLineText'},
    {'name': 'File Type',     'type': 'singleLineText'},
    {'name': 'File Size',     'type': 'singleLineText'},
    {'name': 'Uploaded By',   'type': 'singleLineText'},
    {'name': 'File',          'type': 'multipleAttachments'},
    {'name': 'AI Summary',    'type': 'multilineText'},
])

# ── Franchisee Groups ─────────────────────────────────────────────────────────
create_table('Franchisee Groups',
    'Registry of all franchisee groups and DRAs. Controls the GEN FA group selector.', [
    {'name': 'Group Name',    'type': 'singleLineText'},
    {'name': 'Group ID',      'type': 'singleLineText'},
    {'name': 'Description',   'type': 'singleLineText'},
    {'name': 'Addendum Title','type': 'singleLineText'},
    {'name': 'Token Map',     'type': 'multilineText'},
    {'name': 'Addendum B64',  'type': 'multilineText'},
])

# ── FA Tracker ───────────────────────────────────────────────────────────────
create_table('FA Tracker',
    'Tracks all executed Franchise Agreements, execution dates, expiration dates, and renewal alerts.', [
    {'name': 'Agreement Name',    'type': 'singleLineText'},
    {'name': 'Franchisee Entity', 'type': 'singleLineText'},
    {'name': 'Shop Name',         'type': 'singleLineText'},
    {'name': 'Shop Number',       'type': 'singleLineText'},
    {'name': 'DRA Group',         'type': 'singleLineText'},
    {'name': 'Execution Date',    'type': 'date', 'options': {'dateFormat': {'name': 'iso'}}},
    {'name': 'Expiration Date',   'type': 'date', 'options': {'dateFormat': {'name': 'iso'}}},
    {'name': 'Term Years',        'type': 'number', 'options': {'precision': 0}},
    {'name': 'Status',            'type': 'singleSelect', 'options': {'choices': [
        {'name': 'Active'}, {'name': 'Expiring Soon'}, {'name': 'Expired'}]}},
    {'name': 'Signatory Name',    'type': 'singleLineText'},
    {'name': 'Generated By',      'type': 'singleLineText'},
    {'name': 'Notes',             'type': 'multilineText'},
])

print('\nSetup complete! Copy the table IDs above into the TABLES constant in index.html.\n')
