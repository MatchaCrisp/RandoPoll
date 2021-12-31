--
-- PostgreSQL database dump
--

-- Dumped from database version 14.1
-- Dumped by pg_dump version 14.1

-- Started on 2021-12-31 13:15:17

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 214 (class 1259 OID 24720)
-- Name: fav_cream_quest; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fav_cream_quest (
    que_id integer NOT NULL,
    name text NOT NULL,
    options jsonb NOT NULL,
    is_req boolean NOT NULL
);


ALTER TABLE public.fav_cream_quest OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 24719)
-- Name: fav_cream_quest_que_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fav_cream_quest_que_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fav_cream_quest_que_id_seq OWNER TO postgres;

--
-- TOC entry 3333 (class 0 OID 0)
-- Dependencies: 213
-- Name: fav_cream_quest_que_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.fav_cream_quest_que_id_seq OWNED BY public.fav_cream_quest.que_id;


--
-- TOC entry 212 (class 1259 OID 24711)
-- Name: fav_cream_res; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fav_cream_res (
    res_id integer NOT NULL,
    fav_cream text NOT NULL
);


ALTER TABLE public.fav_cream_res OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 24710)
-- Name: fav_cream_res_res_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fav_cream_res_res_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fav_cream_res_res_id_seq OWNER TO postgres;

--
-- TOC entry 3334 (class 0 OID 0)
-- Dependencies: 211
-- Name: fav_cream_res_res_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.fav_cream_res_res_id_seq OWNED BY public.fav_cream_res.res_id;


--
-- TOC entry 210 (class 1259 OID 24594)
-- Name: polls; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.polls (
    poll_id integer NOT NULL,
    poll_table text NOT NULL,
    surv_table text NOT NULL,
    poll_title text NOT NULL,
    poll_start date NOT NULL,
    poll_end date NOT NULL
);


ALTER TABLE public.polls OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 24593)
-- Name: polls_poll_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.polls_poll_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.polls_poll_id_seq OWNER TO postgres;

--
-- TOC entry 3335 (class 0 OID 0)
-- Dependencies: 209
-- Name: polls_poll_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.polls_poll_id_seq OWNED BY public.polls.poll_id;


--
-- TOC entry 3176 (class 2604 OID 24723)
-- Name: fav_cream_quest que_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fav_cream_quest ALTER COLUMN que_id SET DEFAULT nextval('public.fav_cream_quest_que_id_seq'::regclass);


--
-- TOC entry 3175 (class 2604 OID 24714)
-- Name: fav_cream_res res_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fav_cream_res ALTER COLUMN res_id SET DEFAULT nextval('public.fav_cream_res_res_id_seq'::regclass);


--
-- TOC entry 3174 (class 2604 OID 24597)
-- Name: polls poll_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.polls ALTER COLUMN poll_id SET DEFAULT nextval('public.polls_poll_id_seq'::regclass);


--
-- TOC entry 3327 (class 0 OID 24720)
-- Dependencies: 214
-- Data for Name: fav_cream_quest; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fav_cream_quest (que_id, name, options, is_req) FROM stdin;
1	fav_cream	{"op3_other": {"dispMsg": "other flavor", "inputVal": "othe", "inputType": "radio"}, "op1_vanilla": {"dispMsg": "vanilla", "inputVal": "vani", "inputType": "radio"}, "op4_nothing": {"dispMsg": "not a fan of ice cream", "inputVal": "noth", "inputType": "radio"}, "op2_chocolate": {"dispMsg": "chocolate", "inputVal": "choc", "inputType": "radio"}}	t
\.


--
-- TOC entry 3325 (class 0 OID 24711)
-- Dependencies: 212
-- Data for Name: fav_cream_res; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fav_cream_res (res_id, fav_cream) FROM stdin;
1	choc
3	choc
4	choc
5	choc
6	choc
7	choc
8	choc
9	choc
10	choc
11	choc
12	choc
13	vani
14	vani
15	vani
16	vani
17	vani
18	vani
19	vani
20	vani
21	vani
22	othe
23	othe
24	othe
25	othe
26	othe
27	noth
28	noth
29	noth
30	othe
31	vani
\.


--
-- TOC entry 3323 (class 0 OID 24594)
-- Dependencies: 210
-- Data for Name: polls; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.polls (poll_id, poll_table, surv_table, poll_title, poll_start, poll_end) FROM stdin;
1	fav_cream_res	fav_cream_quest	chocolate_vs_vanilla_ice_cream	2021-12-29	2022-01-05
\.


--
-- TOC entry 3336 (class 0 OID 0)
-- Dependencies: 213
-- Name: fav_cream_quest_que_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fav_cream_quest_que_id_seq', 2, true);


--
-- TOC entry 3337 (class 0 OID 0)
-- Dependencies: 211
-- Name: fav_cream_res_res_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fav_cream_res_res_id_seq', 31, true);


--
-- TOC entry 3338 (class 0 OID 0)
-- Dependencies: 209
-- Name: polls_poll_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.polls_poll_id_seq', 25, true);


--
-- TOC entry 3182 (class 2606 OID 24727)
-- Name: fav_cream_quest fav_cream_quest_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fav_cream_quest
    ADD CONSTRAINT fav_cream_quest_pkey PRIMARY KEY (que_id);


--
-- TOC entry 3180 (class 2606 OID 24718)
-- Name: fav_cream_res fav_cream_res_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fav_cream_res
    ADD CONSTRAINT fav_cream_res_pkey PRIMARY KEY (res_id);


--
-- TOC entry 3178 (class 2606 OID 24601)
-- Name: polls polls_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.polls
    ADD CONSTRAINT polls_pkey PRIMARY KEY (poll_id);


-- Completed on 2021-12-31 13:15:18

--
-- PostgreSQL database dump complete
--

