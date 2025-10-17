CREATE TABLE bonus (
    ename VARCHAR NOT NULL,
    job VARCHAR NOT NULL,
    sal INTEGER NOT NULL,
    comm INTEGER NOT NULL
);

CREATE TABLE dept (
    deptno INTEGER NOT NULL,
    name VARCHAR NOT NULL
);

CREATE TABLE emp (
    empno INTEGER NOT NULL,
    deptno INTEGER NOT NULL,
    ename VARCHAR NOT NULL,
    job VARCHAR NOT NULL,
    mgr INTEGER,
    hiredate DATE NOT NULL,
    sal INTEGER NOT NULL,
    comm INTEGER NOT NULL,
    slacker BOOLEAN NOT NULL
);

CREATE TABLE emp_b (
    empno INTEGER NOT NULL,
    deptno INTEGER NOT NULL,
    ename VARCHAR NOT NULL,
    job VARCHAR NOT NULL,
    mgr INTEGER,
    hiredate DATE NOT NULL,
    sal INTEGER NOT NULL,
    comm INTEGER NOT NULL,
    slacker BOOLEAN NOT NULL,
    birthdate DATE NOT NULL
);

CREATE TABLE empnullables (
    empno INTEGER NOT NULL,
    deptno INTEGER,
    ename VARCHAR,
    job VARCHAR,
    mgr INTEGER,
    hiredate DATE,
    sal INTEGER,
    comm INTEGER,
    slacker BOOLEAN
);

CREATE TABLE empnullables_20 (
    empno INTEGER NOT NULL,
    deptno INTEGER,
    ename VARCHAR,
    job VARCHAR,
    mgr INTEGER,
    hiredate DATE,
    sal INTEGER,
    comm INTEGER,
    slacker BOOLEAN
);


ALTER TABLE dept ADD CONSTRAINT dept_pkey PRIMARY KEY (deptno);
ALTER TABLE emp ADD CONSTRAINT emp_pkey PRIMARY KEY (empno);
ALTER TABLE emp_b ADD CONSTRAINT emp_b_pkey PRIMARY KEY (empno);
ALTER TABLE empnullables ADD CONSTRAINT empnullables_pkey PRIMARY KEY (empno);
ALTER TABLE empnullables_20 ADD CONSTRAINT empnullables_20_pkey PRIMARY KEY (empno);
