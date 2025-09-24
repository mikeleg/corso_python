# Day #2 Corso python


## API: Paginazione vs Slice

### Rotte Paginate
Tutte le rotte GET che restituiscono liste supportano la paginazione tramite i parametri `page` e `per_page`.

**Parametri**
- `page`: numero della pagina (default: 1)
- `per_page`: elementi per pagina (default: 10, min: 1, max: 100)

**Esempio di risposta**
```json
{
	"data": [...],
	"page": 1,
	"per_page": 10,
	"total": 123,
	"total_pages": 13
}
```

Le nuove rotte GET future erediteranno automaticamente la paginazione centralizzata.

### Rotte Slice
Le rotte `/resource/slice` restituiscono una "fetta" di dati senza metadati di paginazione.

**Parametri**
- `start`: indice iniziale (inclusivo, default: 0)
- `end`: indice finale (esclusivo, default: 10)

**Esempio di risposta**
```json
[
	{ ... },
	{ ... }
]
```

**Differenze principali**
- Le rotte paginated (`/resource/`) restituiscono dati e metadati (pagina, totale, ecc.).
- Le rotte slice (`/resource/slice`) restituiscono solo la lista dei dati richiesti, senza metainformazioni.
- Le slice sono utili quando servono solo i dati, senza informazioni aggiuntive di paginazione.

## Architettura

La logica di business della paginazione è separata dai router e gestita tramite un usecase dedicato (`app/usecases/pagination.py`).

I router si occupano solo di orchestrare la richiesta e delegano la logica di estrazione e paginazione dei dati ai casi d'uso, secondo i principi della Clean Architecture.

Questo rende il codice facilmente estendibile, testabile e manutenibile.

## Clean Architecture CRUD

Tutte le operazioni CRUD (Create, Read, Update, Delete) sono gestite tramite usecase dedicati in `app/usecases/`. I router si limitano a orchestrare la richiesta e delegare la logica di business ai casi d'uso, garantendo separazione delle responsabilità e facilità di test.

Esempi di usecase:
- `CreateEntityUseCase`
- `GetEntityUseCase`
- `UpdateEntityUseCase`
- `DeleteEntityUseCase`

Questa struttura rende il progetto facilmente estendibile e manutenibile.


## Run Application

Per avviare l'applicazione FastAPI:

```bash
uvicorn app.main:app --reload
```

L'app sarà disponibile su http://127.0.0.1:8000

Per la documentazione interattiva: http://127.0.0.1:8000/docs
