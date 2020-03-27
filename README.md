# Listle

An easy back-end for collecting arbitrary information for an email list or campaign.

### Records
Records are the main object of Listle. Any time you call to Listle it will transform the request into the record format. However, Listle doesn't do anything with these records immediately. Instead, it relies on record-managers to handle the incoming data.

### Objects
* Record
* RecordManager

## Endpoints

### POST `/`

Create a record
