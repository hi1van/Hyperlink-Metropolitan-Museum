--
-- PostgreSQL database dump
--

-- Dumped from database version 14.15 (Homebrew)
-- Dumped by pg_dump version 14.15 (Homebrew)

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
-- Name: Art; Type: TABLE; Schema: public; Owner: ivanzhuang
--

CREATE TABLE public."Art" (
    id integer NOT NULL,
    "objectID" integer NOT NULL,
    "primaryImage" character varying NOT NULL,
    artist character varying,
    artist_bio character varying,
    artwork_date character varying,
    medium character varying,
    dimensions character varying,
    department character varying,
    object_name character varying,
    title character varying,
    period character varying
);


ALTER TABLE public."Art" OWNER TO ivanzhuang;

--
-- Name: Art_id_seq; Type: SEQUENCE; Schema: public; Owner: ivanzhuang
--

CREATE SEQUENCE public."Art_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Art_id_seq" OWNER TO ivanzhuang;

--
-- Name: Art_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ivanzhuang
--

ALTER SEQUENCE public."Art_id_seq" OWNED BY public."Art".id;


--
-- Name: User; Type: TABLE; Schema: public; Owner: ivanzhuang
--

CREATE TABLE public."User" (
    id integer NOT NULL,
    username character varying(50) NOT NULL
);


ALTER TABLE public."User" OWNER TO ivanzhuang;

--
-- Name: User_id_seq; Type: SEQUENCE; Schema: public; Owner: ivanzhuang
--

CREATE SEQUENCE public."User_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."User_id_seq" OWNER TO ivanzhuang;

--
-- Name: User_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ivanzhuang
--

ALTER SEQUENCE public."User_id_seq" OWNED BY public."User".id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: flask_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO flask_user;

--
-- Name: user_art_favourites; Type: TABLE; Schema: public; Owner: ivanzhuang
--

CREATE TABLE public.user_art_favourites (
    user_id integer NOT NULL,
    art_id integer NOT NULL
);


ALTER TABLE public.user_art_favourites OWNER TO ivanzhuang;

--
-- Name: Art id; Type: DEFAULT; Schema: public; Owner: ivanzhuang
--

ALTER TABLE ONLY public."Art" ALTER COLUMN id SET DEFAULT nextval('public."Art_id_seq"'::regclass);


--
-- Name: User id; Type: DEFAULT; Schema: public; Owner: ivanzhuang
--

ALTER TABLE ONLY public."User" ALTER COLUMN id SET DEFAULT nextval('public."User_id_seq"'::regclass);


--
-- Data for Name: Art; Type: TABLE DATA; Schema: public; Owner: ivanzhuang
--

COPY public."Art" (id, "objectID", "primaryImage", artist, artist_bio, artwork_date, medium, dimensions, department, object_name, title, period) FROM stdin;
\.


--
-- Data for Name: User; Type: TABLE DATA; Schema: public; Owner: ivanzhuang
--

COPY public."User" (id, username) FROM stdin;
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: flask_user
--

COPY public.alembic_version (version_num) FROM stdin;
19bd5eeb08e6
\.


--
-- Data for Name: user_art_favourites; Type: TABLE DATA; Schema: public; Owner: ivanzhuang
--

COPY public.user_art_favourites (user_id, art_id) FROM stdin;
\.


--
-- Name: Art_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ivanzhuang
--

SELECT pg_catalog.setval('public."Art_id_seq"', 1, false);


--
-- Name: User_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ivanzhuang
--

SELECT pg_catalog.setval('public."User_id_seq"', 1, false);


--
-- Name: Art Art_pkey; Type: CONSTRAINT; Schema: public; Owner: ivanzhuang
--

ALTER TABLE ONLY public."Art"
    ADD CONSTRAINT "Art_pkey" PRIMARY KEY (id);


--
-- Name: User User_pkey; Type: CONSTRAINT; Schema: public; Owner: ivanzhuang
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (id);


--
-- Name: User User_username_key; Type: CONSTRAINT; Schema: public; Owner: ivanzhuang
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_username_key" UNIQUE (username);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: flask_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: user_art_favourites user_art_favourites_pkey; Type: CONSTRAINT; Schema: public; Owner: ivanzhuang
--

ALTER TABLE ONLY public.user_art_favourites
    ADD CONSTRAINT user_art_favourites_pkey PRIMARY KEY (user_id, art_id);


--
-- Name: user_art_favourites user_art_favourites_art_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ivanzhuang
--

ALTER TABLE ONLY public.user_art_favourites
    ADD CONSTRAINT user_art_favourites_art_id_fkey FOREIGN KEY (art_id) REFERENCES public."Art"(id);


--
-- Name: user_art_favourites user_art_favourites_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ivanzhuang
--

ALTER TABLE ONLY public.user_art_favourites
    ADD CONSTRAINT user_art_favourites_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."User"(id);


--
-- PostgreSQL database dump complete
--

