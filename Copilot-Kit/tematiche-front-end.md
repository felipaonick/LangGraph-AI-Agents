# FRONT-END

Possiamo passare molto tempo nel back-end costruendo il nostro agente e costruendo 
il nostro sistema di RAG e assicuraci che l'output che diamo all'utente sia l'output corretto, che sia attendibile e di qualità.

Senza dubbio, questi sono solo alcuni pezzi del puzzle.

Per far si che la nostra applicazione sia completa dobbiamo creare una user interface bella ed una user experience molto naturale per i nostri utenti.

La fiducia tra gli users e le generative AI applications e qualcosa su cui dobbiamo lavorare, poiché gli utenti sanno che le 
applicazioni generative non sempre sono affidabili e non sempre danno le risposte corrette e a volte possono fallire.

Per far ciò correttamente è una grande sfida.

# COPILOT KIT

È un open-source che ci aiuterà nella creazione di interfacce belle, ma più importante, avere esperienze utente più naturali nelle nostre applicazioni di generative AI.

Copilot kit ci offre i migliori building-box per costruire una bella user interface.

Quando parliamo di User Interface UI generativa, ci riferiamo, in generale, all'interfaccia con gli utenti della nostra applicazione la quale si basa sugli LLMs.

# Trasparenza --> Affidabilità

Per creare affidabilità tra gli utenti e il nostro sistema dobbiamo essere trasparenti.

L'utente deve sapere da dove arriva la risposta, ad esempio, se stiamo costruendo un agente, dobbiamo essere trasparenti riguardo a quali tools l'agente ha a disposizione e quali utilizza per generare la risposta, e perché ha scelto di usare tale tool.

Quindi il ragionamento dell'agente può consistere in alcuni calcoli intermedi fino a ottenere la risposta finale.

E dobbiamo far si che possiamo vedere come si elabora la risposta finale.

Incluso in una applicazione RAG, dobbiamo essere trasparenti e mostrare all'utente quali Documents abbiamo utilizzato per generare la risposta finale, per far si che l'utente sappia da dove viene.

Tutto questo va a creare una maggiore fiducia tra gli utenti e la nostra applicazione di AI generativa.

# Parliamo di COPILOTKIT

Secondo alcuni esperti, sono i pionieri nel panorama della user interface generativa e nell user experience generativa

Nella sua documentazione [CopilotKit Docs](https://docs.copilotkit.ai/quickstart) vediamo che introducono un bunch di componenti e hooks che possiamo utilizzare facilmente nei nostri front-ends, 
il che rende superfacile costruire una Generativa UI e costruire user experience molto buone costruite sulle nostre applicazioni di AI generativa, che è costruita con langchain, langgraph ecc.

Approfondiamo la compatibilità con le applicazioni langchain e langgraph e introdurre i **co-agents** che si integrano alla perfezione con i langgraph back-ends.

Quando abbiamo una applicazione LangGraph avvengono molte cose e molte parti mobili, abbiamo lo **stato** del grafo che cambia costantemente, abbiamo i risultati intermedi in tale stato.
Abbiamo i nodi che si eseguono, e forse si eseguono anche in parallelo. Inoltre abbiamo lo **human-in-the-loop** dove si arresta l'esecuzione del grafo e andiamo a prendere l'input dell'utente, e poi possiamo ritornare a rieseguire il grafo.

Dunque con una applicazione back-end con tutte queste parti mobili costruire il front-end diventa un'incubo.

Con Copilotkit invece possiamo implementare componenti per tutto ciò che abbiamo discusso precedentemente in LangGraph, tutte per essere costruite su applicazioni LangGraph 

