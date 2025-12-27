import os
import imaplib
import email
from email.header import decode_header
from typing import List, Dict, Any, Optional


class ImapConnectionError(Exception):
    """Errore di connessione IMAP."""
    pass


class ImapReader:
    """
    Lettore IMAP generico per Microsoft 365.

    - Usa le variabili d'ambiente:
        IMAP_HOST
        IMAP_PORT
        IMAP_SSL
        EMAIL_USER
        EMAIL_PASSWORD

    - Connessione in sola lettura (read-only)
    - Recupera le email dalla INBOX
    """

    def __init__(self):
        self.host = os.getenv("IMAP_HOST", "outlook.office365.com")
        self.port = int(os.getenv("IMAP_PORT", "993"))
        self.use_ssl = os.getenv("IMAP_SSL", "true").lower() == "true"
        self.username = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PASSWORD")

        if not self.username or not self.password:
            raise ImapConnectionError("EMAIL_USER o EMAIL_PASSWORD non sono impostate nelle variabili d'ambiente.")

        self.connection: Optional[imaplib.IMAP4_SSL] = None

    def connect(self):
        """Apre la connessione IMAP in sola lettura."""
        try:
            if self.use_ssl:
                self.connection = imaplib.IMAP4_SSL(self.host, self.port)
            else:
                self.connection = imaplib.IMAP4(self.host, self.port)

            self.connection.login(self.username, self.password)

            # Selezioniamo INBOX in sola lettura
            status, _ = self.connection.select("INBOX", readonly=True)
            if status != "OK":
                raise ImapConnectionError("Impossibile selezionare la cartella INBOX in modalità read-only.")
        except imaplib.IMAP4.error as e:
            raise ImapConnectionError(f"Errore IMAP durante la connessione o login: {e}") from e

    def close(self):
        """Chiude la connessione IMAP."""
        if self.connection is not None:
            try:
                self.connection.close()
            except Exception:
                # Alcuni server potrebbero già avere la mailbox chiusa
                pass
            finally:
                self.connection.logout()
                self.connection = None

    def _decode_header_value(self, value: Any) -> str:
        """Decodifica correttamente l'header (es. Subject)."""
        if not value:
            return ""

        decoded_parts = decode_header(value)
        parts: List[str] = []

        for text, enc in decoded_parts:
            if isinstance(text, bytes):
                try:
                    parts.append(text.decode(enc or "utf-8", errors="ignore"))
                except LookupError:
                    parts.append(text.decode("utf-8", errors="ignore"))
            else:
                parts.append(str(text))

        return " ".join(parts).strip()

    def _get_email_body(self, msg: email.message.Message) -> str:
        """Estrae il corpo testuale (preferibilmente text/plain)."""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                disposition = str(part.get("Content-Disposition", "")).lower()

                if "attachment" in disposition:
                    continue

                if content_type == "text/plain":
                    try:
                        return part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", errors="ignore")
                    except Exception:
                        continue

            # fallback su text/html se proprio non c'è altro
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/html":
                    try:
                        return part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", errors="ignore")
                    except Exception:
                        continue
        else:
            if msg.get_content_type() in ("text/plain", "text/html"):
                try:
                    return msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8", errors="ignore")
                except Exception:
                    return ""

        return ""

    def fetch_last_emails(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Recupera le ultime N email dalla INBOX (ordine dalla più recente).

        Ritorna una lista di dizionari con:
        - id: uid del messaggio
        - subject
        - from
        - date
        - body
        """
        if self.connection is None:
            raise ImapConnectionError("Connessione IMAP non aperta. Chiama prima connect().")

        status, data = self.connection.search(None, "ALL")
        if status != "OK":
            raise ImapConnectionError("Errore nella ricerca dei messaggi in INBOX.")

        # Lista di ID messaggi
        message_ids = data[0].split()
        # Prendiamo solo gli ultimi `limit`
        message_ids = message_ids[-limit:]

        emails: List[Dict[str, Any]] = []

        for msg_id in message_ids:
            status, msg_data = self.connection.fetch(msg_id, "(RFC822)")
            if status != "OK" or not msg_data or msg_data[0] is None:
                continue

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject = self._decode_header_value(msg.get("Subject"))
            from_ = self._decode_header_value(msg.get("From"))
            date_ = self._decode_header_value(msg.get("Date"))
            body = self._get_email_body(msg)

            emails.append(
                {
                    "id": msg_id.decode("utf-8"),
                    "subject": subject,
                    "from": from_,
                    "date": date_,
                    "body": body,
                }
            )

        return emails

    def fetch_unseen_emails(self) -> List[Dict[str, Any]]:
        """
        Recupera le email non lette (UNSEEN).

        Anche qui ritorna una lista di dict come fetch_last_emails.
        """
        if self.connection is None:
            raise ImapConnectionError("Connessione IMAP non aperta. Chiama prima connect().")

        status, data = self.connection.search(None, "UNSEEN")
        if status != "OK":
            raise ImapConnectionError("Errore nella ricerca delle email UNSEEN.")

        message_ids = data[0].split()
        emails: List[Dict[str, Any]] = []

        for msg_id in message_ids:
            status, msg_data = self.connection.fetch(msg_id, "(RFC822)")
            if status != "OK" or not msg_data or msg_data[0] is None:
                continue

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject = self._decode_header_value(msg.get("Subject"))
            from_ = self._decode_header_value(msg.get("From"))
            date_ = self._decode_header_value(msg.get("Date"))
            body = self._get_email_body(msg)

            emails.append(
                {
                    "id": msg_id.decode("utf-8"),
                    "subject": subject,
                    "from": from_,
                    "date": date_,
                    "body": body,
                }
            )

        return emails


# Esempio d'uso standalone (per debug manuale)
if __name__ == "__main__":
    reader = ImapReader()
    try:
        reader.connect()
        mails = reader.fetch_last_emails(limit=5)
        print(f"Trovate {len(mails)} email.")
        for m in mails:
            print("=" * 60)
            print("ID:     ", m["id"])
            print("From:   ", m["from"])
            print("Subject:", m["subject"])
            print("Date:   ", m["date"])
            print("Body:\n", m["body"][:500], "...")
    except ImapConnectionError as e:
        print("Errore IMAP:", e)
    finally:
        reader.close()
