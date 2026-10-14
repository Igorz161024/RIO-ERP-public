--
-- PostgreSQL database dump
--

\restrict m24uVlnX9aVuaGz8k6DgkEsw7xrFgMdD4iNmifoB8tHriDtt1lVRHgMSNPxLHwa

-- Dumped from database version 18.4 (Debian 18.4-1.pgdg13+1)
-- Dumped by pg_dump version 18.4 (Debian 18.4-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, email, password_hash, role, refresh_token) FROM stdin;
6	user	user@example.com	b2	user	\N
7	auditor	auditor@example.com	b2	auditor	\N
5	admin	admin@example.com	$2b$12$GB89f8ubJ/QDL/W91EOzo.C4H2L7.MmXpvRwu2XIhn/CXMb.ANYV2	admin	\N
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 8, true);


--
-- PostgreSQL database dump complete
--

\unrestrict m24uVlnX9aVuaGz8k6DgkEsw7xrFgMdD4iNmifoB8tHriDtt1lVRHgMSNPxLHwa

