grammar llull;


// Funcio que es crida a l'inici
root : program EOF ;

program: ENTER* (void ENTER*)* ENTER* voidmain? ENTER* (void ENTER*)* ;

void : VOID ID v_id OPEN_CLAU bloc CLOSE_CLAU ;
voidmain : VOID MAIN v_id OPEN_CLAU bloc CLOSE_CLAU ;
v_id : OPEN_PAR (ID (COMA ID)*)? CLOSE_PAR ;


// Un bloc es un conjunt de sentencies
bloc : sentence* ;

// Una sentencia pot ser dels seguents tipus
sentence
    : assig_sent
    | f_sent
    | write_sent
    | read_sent
    | if_sent
    | while_sent
    | for_sent
    | arrayop
    | setarray
    | coment
    | ENTER
    ;




// Formes que pot tenir una expresio
expr
    : OPEN_PAR expr CLOSE_PAR
    | expr MULT expr
    | expr DIV expr 
    | expr MOD expr
    | expr MES expr
    | expr MENYS expr
    | expr GT expr
    | expr LT expr
    | expr GEQ expr
    | expr LEQ expr
    | expr EQ expr
    | expr NEQ expr
    | INT
    | FLOAT
    | TEXT
    | ID
    | getarray
    ;

//Sentencies de taules
arrayop : ARRAY OPEN_PAR ID COMA expr CLOSE_PAR;
getarray : GET OPEN_PAR ID COMA expr CLOSE_PAR;
setarray : SET OPEN_PAR ID COMA expr COMA expr CLOSE_PAR;


// Sentencia que fa una crida a una funcio
f_sent : ID OPEN_PAR p_exec CLOSE_PAR ;
p_exec : (expr (COMA expr)*)? ;


// Sentencies d'assignacio i d'E/S
assig_sent : ID ASSIG expr ;
read_sent : READ OPEN_PAR ID CLOSE_PAR ;
write_sent : WRITE OPEN_PAR w_expr CLOSE_PAR;
w_expr : expr (COMA expr)* ;


// Sentecies condicional i dels bucles
if_sent : IF OPEN_PAR expr CLOSE_PAR OPEN_CLAU bloc CLOSE_CLAU (ELSE OPEN_CLAU bloc CLOSE_CLAU)?;

while_sent : WHILE OPEN_PAR expr CLOSE_PAR OPEN_CLAU bloc CLOSE_CLAU ;

for_sent : FOR OPEN_PAR assig_sent PUNTCOMA expr PUNTCOMA assig_sent CLOSE_PAR OPEN_CLAU bloc CLOSE_CLAU ;


// Comentaris
coment : COM (expr|sentence)* ENTER ;


// Operadors Aritmetics
    MES : '+' ;
    MENYS: '-' ;
    MULT: '*' ;
    DIV: '/' ;
    MOD: '%' ;

// Operadors Logics
    GT: '>';
    LT: '<';
    GEQ: '>=';
    LEQ: '<=';
    EQ: '==';
    NEQ: '<>';


// Operador d'assignacio

    ASSIG: '=';

    PUNTCOMA: ';' ;
    COMA: ',' ;

// Operadors d'E/S
    READ: 'read';
    WRITE: 'write';


// Sentencia Condicional
    IF: 'if';
    ELSE: 'else';


// Bucles
    WHILE: 'while';
    FOR: 'for';


// Comentaris

    COM: '#' ;

// Taules

    GET: 'get' ;
    SET: 'set' ;
    ARRAY: 'array' ;

// Funcio main i funcions

    MAIN: 'main' ;
    VOID: 'void' ;

// Parentesis
    OPEN_PAR: '(' ;
    CLOSE_PAR: ')' ;
    OPEN_CLAU: '{' ;
    CLOSE_CLAU: '}' ;



// Tipus de valors
    INT: [0-9]+ ;
    FLOAT: [0-9]+ '.' [0-9]* ;
    TEXT : '"'(~'"')+'"';
    ID: [a-zA-Z][a-zA-Z_0-9]* ;
    ENTER : [\n\r];
    WS : [ \t\n]+ -> skip;


