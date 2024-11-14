SELECT 
    Benutzer.UserID,
    Benutzer.Vorname,
    Benutzer.Nachname,
    Benutzer.EMail,
    Umfrage.SurveyID,
    Umfrage.Titel AS UmfrageTitel,
    Umfrage.Beschreibung AS UmfrageBeschreibung,
    Frage.QuestionID,
    Frage.Fragetext,
    Frage.Fragetyp,
    Antwort.Antwortdatum,
    Antwortoption.OptionID,
    Antwortoption.Optionstext,
    Antwortdetail.Freitextantwort
FROM 
    Antwort
JOIN 
    Benutzer ON Antwort.UserID = Benutzer.UserID
JOIN 
    Umfrage ON Antwort.SurveyID = Umfrage.SurveyID
JOIN 
    Antwortdetail ON Antwort.ResponseID = Antwortdetail.ResponseID
JOIN 
    Frage ON Antwortdetail.QuestionID = Frage.QuestionID
LEFT JOIN 
    Antwortoption ON Antwortdetail.OptionID = Antwortoption.OptionID
WHERE 
    Benutzer.UserID = 1;  -- Ersetzen Sie die 1 durch die UserID des gewünschten Nutzers



-+----------+------------------+---------------------------+------------+----------------------------+--------------+--------------+----------+-------------+-----------------+
| UserID | Vorname | Nachname | EMail                 | SurveyID | UmfrageTitel     | UmfrageBeschreibung       | QuestionID | Fragetext                  | Fragetyp     | Antwortdatum | OptionID | Optionstext | Freitextantwort |
+--------+---------+----------+-----------------------+----------+------------------+---------------------------+------------+----------------------------+--------------+--------------+----------+-------------+-----------------+
|      2 | Test    | User     | test.user@example.com |        1 | Beispiel Umfrage | Dies ist eine Testumfrage |          1 | Welche Anwort ist richtig? | SingleChoice | 2024-11-14   |        2 | B           | NULL            |
+--------+---------+----------+-----------------------+----------+------------------+---------------------------+------------+----------------------------+--------------+--------------+----------+-------------+-----------------+
