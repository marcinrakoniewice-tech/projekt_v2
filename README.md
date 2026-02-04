Zadaniem programu jest wykonywanie backtestów, dla pomysłów inwestycyjnych opartych o:
+ wskażniki fundamentalne
+ ruch ceny
+ wslażniki techniczne

Obecny stan, to stan początkowy twtworzę szkielet aplikacji:
+ W repo zdalnym jest umieszony kod ściągający dane dla interwałów dziennych wybranego indeksu, 20 lat wstecz,
Na gałęzi pobocznej wysłałem kod aplikacji robiącej, prosty test strategii opierającej się o przecięcie średnich.

Plany są takie by:
+ aplikacja robiła znacznie bardziej skomplikowane backtesty dla wybranych spółek i indeksów, w różnych interwałach czasowych z wykorzystaniem wsk. fundamentalnych i technicznych;
+ wykorzystać langfuse do monitoringu;
+ wykorzystać streamlit do wprowadzenia warunków strategii i wizualizacji danych z backtestów.
+ jest kilka pomysłów innych ale pierw trzeba ogarnąć to co wyżej.