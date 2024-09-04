# StarWars-AntiMisiles-System
Trabajo de Fin de Grado para la Titulación de Ingeniería Informática por la Universidad de Granada - Nota Final: 8.8 sobre 10

El software que voy a desarrollar es un simulador, concretamente de un sistema antimisiles.

El simulador se corresponde con un escenario en el cual un sistema antimisiles debe defender un mapa de continuos ataques con misiles a ciertos puntos estrat ́egicos diferenciados en el mapa(ciudades, bases militares, etc...).
Estos lugares estrat ́egicos se representaran en el mapa a traves de la interfaz grafica del software y seran vitales para comprobar la eficacia del sistema antimisiles.

Los lugares estrat ́egicos nombrados anteriormente ser ́an atacados por misiles Aire-Tierra, es decir, misiles que aparecer ́an en el aire con direccion auno de los multiples lugares estrat ́egicos del mapa. Estos misiles dispondran de multiples valores fısicos como son altura, posicion, velocidad, direccion, etc.

Si uno de los misiles atacantes impacta en un lugar estrat ́egico del mapa, el lugar estrat ́egico sera danado y tras recibir un numero concreto de impactos, este sera finalmente destruido.
Para evitar la destruccion de los lugares estrat ́egicos del mapa entrarıa en accion el sistema antimisiles. Este sistema se compone de 3 subsistemas que son los siguientes:

Subsistema de Radar: Este componente se encargar ́a de ir analizando el mapa en busca de misiles que entren en su rango de accion, permitiendo de esa manera comunicar sus datos actualizados al subsistema de Calculo

Subsistema de Calculo: Este componente se encargara de una vez recibida la informacion por parte del Subsistema de Radar, realizar las asignaciones de subsistemas de contra-medidas a misiles detectados y con ello se enviaran las posiciones de interceptaci ́on actualizadas en todo momento.

Subsistema de Contra-medidas: Este componente se encargara de lanzar un misil interceptor con una ruta directa objetivo la cual se ira actualizando a cada momento gracias a los datos que recibira del subsistema de Calculo. Ademas, se espera la presencia de mas de un misil enemigo actuando a la vez y tambien que pueda haber mas de un Subsistema de contra-medidas que se encargue de la interceptacion de los misiles.

Finalmente, es importante recalcar que el proyecto se va a desarrollar siguiendo la metodologıa agil de SCRUM, esta permitira mantener una buena organizacion y planificacion del proyecto.
