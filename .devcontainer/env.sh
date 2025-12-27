#!/bin/bash

#############################################
# CONFIGURAZIONE EMAIL MICROSOFT 365 (IMAP)
#############################################

# Server IMAP Microsoft 365
export IMAP_HOST="outlook.office365.com"
export IMAP_PORT="993"
export IMAP_SSL="true"

#############################################
# CONFIGURAZIONE EMAIL MICROSOFT 365 (SMTP)
#############################################

# Server SMTP Microsoft 365
export SMTP_HOST="smtp.office365.com"
export SMTP_PORT="587"
export SMTP_STARTTLS="true"

#############################################
# CREDENZIALI EMAIL
#############################################

# Indirizzo email Microsoft 365 usato dal backend
export EMAIL_USER="prenotazioni@lockandfly.com"

# Inserisci qui la PASSWORD PER LE APP (non la password normale)
export EMAIL_PASSWORD="INSERISCI_PASSWORD_APP_QUI"

#############################################
# CONFIGURAZIONE FASTAPI / AMBIENTE
#############################################

export ENVIRONMENT="development"
export DEBUG="true"

#############################################
# DATABASE
#############################################

# SQLite (default)
export DATABASE_URL="sqlite:///./data.db"

# PostgreSQL (per futuro)
# export DATABASE_URL="postgresql://user:password@host:5432/dbname"

#############################################
# ALTRE VARIABILI FUTURE
#############################################

# export API_KEY=""
# export SECRET_KEY=""
# export LOG_LEVEL="info"
