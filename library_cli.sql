--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2
-- Dumped by pg_dump version 15.2

-- Started on 2023-04-07 02:49:34

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
-- TOC entry 214 (class 1259 OID 17928)
-- Name: book; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book (
    book_id integer NOT NULL,
    isbn bigint,
    book_name character varying(150) NOT NULL,
    author character varying(100) NOT NULL,
    pages bigint NOT NULL,
    genre character varying(100),
    num_of_copy bigint,
    added_by character varying(100),
    add_date date DEFAULT CURRENT_DATE
);


ALTER TABLE public.book OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 17932)
-- Name: book_book_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.book_book_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.book_book_id_seq OWNER TO postgres;

--
-- TOC entry 3353 (class 0 OID 0)
-- Dependencies: 215
-- Name: book_book_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.book_book_id_seq OWNED BY public.book.book_id;


--
-- TOC entry 216 (class 1259 OID 17933)
-- Name: borrowing; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.borrowing (
    borrow_id integer NOT NULL,
    customer_id bigint NOT NULL,
    book_id bigint NOT NULL,
    borowing_date date DEFAULT CURRENT_DATE,
    return_date date,
    is_returned boolean DEFAULT false,
    is_favorite boolean DEFAULT false,
    rating numeric(3,2),
    is_read boolean DEFAULT false
);


ALTER TABLE public.borrowing OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 17940)
-- Name: borrowing_borrow_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.borrowing_borrow_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.borrowing_borrow_id_seq OWNER TO postgres;

--
-- TOC entry 3354 (class 0 OID 0)
-- Dependencies: 217
-- Name: borrowing_borrow_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.borrowing_borrow_id_seq OWNED BY public.borrowing.borrow_id;


--
-- TOC entry 218 (class 1259 OID 17941)
-- Name: customer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customer (
    customer_id integer NOT NULL,
    first_name character varying(40),
    last_name character varying(40),
    phone character varying(40),
    email character varying(40),
    username character varying(40) NOT NULL,
    password character varying(40) NOT NULL,
    is_logined boolean DEFAULT false
);


ALTER TABLE public.customer OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 17945)
-- Name: customer_customer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.customer_customer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.customer_customer_id_seq OWNER TO postgres;

--
-- TOC entry 3355 (class 0 OID 0)
-- Dependencies: 219
-- Name: customer_customer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.customer_customer_id_seq OWNED BY public.customer.customer_id;


--
-- TOC entry 3183 (class 2604 OID 17946)
-- Name: book book_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book ALTER COLUMN book_id SET DEFAULT nextval('public.book_book_id_seq'::regclass);


--
-- TOC entry 3185 (class 2604 OID 17947)
-- Name: borrowing borrow_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.borrowing ALTER COLUMN borrow_id SET DEFAULT nextval('public.borrowing_borrow_id_seq'::regclass);


--
-- TOC entry 3190 (class 2604 OID 17948)
-- Name: customer customer_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customer ALTER COLUMN customer_id SET DEFAULT nextval('public.customer_customer_id_seq'::regclass);


--
-- TOC entry 3342 (class 0 OID 17928)
-- Dependencies: 214
-- Data for Name: book; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.book (book_id, isbn, book_name, author, pages, genre, num_of_copy, added_by, add_date) VALUES (1, 348939, 'The Alchemist', 'Paulo Coelho', 161, 'Fiction', 6, NULL, '2023-04-02');
INSERT INTO public.book (book_id, isbn, book_name, author, pages, genre, num_of_copy, added_by, add_date) VALUES (2, 589398, 'The Invisible Man', 'Agatha Christie', 188, 'Detective', 3, NULL, '2023-04-02');
INSERT INTO public.book (book_id, isbn, book_name, author, pages, genre, num_of_copy, added_by, add_date) VALUES (5, 389902, 'Once There Was', 'Kiyash Monsef', 232, 'Romance', 1, NULL, '2023-04-03');
INSERT INTO public.book (book_id, isbn, book_name, author, pages, genre, num_of_copy, added_by, add_date) VALUES (6, 120930, 'The Middle Stories', 'Sol Stein', 326, 'Classic', 1, NULL, '2023-04-05');
INSERT INTO public.book (book_id, isbn, book_name, author, pages, genre, num_of_copy, added_by, add_date) VALUES (7, 598930, 'Tell No One', 'Tom Clancy', 431, 'Thrillers', 3, NULL, '2023-04-05');
INSERT INTO public.book (book_id, isbn, book_name, author, pages, genre, num_of_copy, added_by, add_date) VALUES (9, 39033, 'The Element of Fire', 'Martha Wells', 121, 'History', 1, NULL, '2023-04-05');
INSERT INTO public.book (book_id, isbn, book_name, author, pages, genre, num_of_copy, added_by, add_date) VALUES (10, 560903, 'The Secret', 'Rhonda Byrne', 182, 'Self-Help', 5, NULL, '2023-04-05');
INSERT INTO public.book (book_id, isbn, book_name, author, pages, genre, num_of_copy, added_by, add_date) VALUES (8, 598695, 'Out of the Blue', 'Joseph Springer', 329, 'Poetry', 1, NULL, '2023-04-05');
INSERT INTO public.book (book_id, isbn, book_name, author, pages, genre, num_of_copy, added_by, add_date) VALUES (11, 589493, 'The Hunger Games', 'The Hunger Games', 188, 'Sci-Fi', 3, NULL, '2023-04-02');
INSERT INTO public.book (book_id, isbn, book_name, author, pages, genre, num_of_copy, added_by, add_date) VALUES (12, 958894, 'Spy', 'Paulo Coelho', 263, 'Fiction', 6, NULL, '2023-04-02');
INSERT INTO public.book (book_id, isbn, book_name, author, pages, genre, num_of_copy, added_by, add_date) VALUES (14, 394030, 'Years of Solitude', 'Mark Bond', 151, 'Suspense', 1, NULL, '2023-04-05');
INSERT INTO public.book (book_id, isbn, book_name, author, pages, genre, num_of_copy, added_by, add_date) VALUES (15, 239090, 'Gone Girl', 'John Walls', 298, 'Thrilles', 5, NULL, '2023-04-05');
INSERT INTO public.book (book_id, isbn, book_name, author, pages, genre, num_of_copy, added_by, add_date) VALUES (16, 509609, 'Père Goriot', 'Charles Dickens', 121, 'Poetry', 1, NULL, '2023-04-05');
INSERT INTO public.book (book_id, isbn, book_name, author, pages, genre, num_of_copy, added_by, add_date) VALUES (17, 229033, 'French Cooking', 'Elizabeth Gilbert', 1, 'Cookbooks', 1, NULL, '2023-04-05');
INSERT INTO public.book (book_id, isbn, book_name, author, pages, genre, num_of_copy, added_by, add_date) VALUES (18, 203092, 'Frida', 'Isaac Asimov', 2, 'True Crime', 3, NULL, '2023-04-05');
INSERT INTO public.book (book_id, isbn, book_name, author, pages, genre, num_of_copy, added_by, add_date) VALUES (13, 90390, 'Royal Holiday', 'Nolan James', 232, 'History', 1, NULL, '2023-04-03');
INSERT INTO public.book (book_id, isbn, book_name, author, pages, genre, num_of_copy, added_by, add_date) VALUES (19, NULL, 'Ww2', 'Adam Lee', 545, 'History', 1, NULL, '2023-04-07');


--
-- TOC entry 3344 (class 0 OID 17933)
-- Dependencies: 216
-- Data for Name: borrowing; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.borrowing (borrow_id, customer_id, book_id, borowing_date, return_date, is_returned, is_favorite, rating, is_read) VALUES (1, 5, 1, '2023-04-03', '2023-05-03', true, true, 0.00, true);
INSERT INTO public.borrowing (borrow_id, customer_id, book_id, borowing_date, return_date, is_returned, is_favorite, rating, is_read) VALUES (5, 13, 6, '2023-04-05', '2023-04-05', true, false, NULL, true);
INSERT INTO public.borrowing (borrow_id, customer_id, book_id, borowing_date, return_date, is_returned, is_favorite, rating, is_read) VALUES (2, 6, 2, '2023-04-03', '2023-04-03', true, false, 0.00, false);
INSERT INTO public.borrowing (borrow_id, customer_id, book_id, borowing_date, return_date, is_returned, is_favorite, rating, is_read) VALUES (8, 13, 8, '2023-04-05', '2023-04-05', true, false, NULL, true);
INSERT INTO public.borrowing (borrow_id, customer_id, book_id, borowing_date, return_date, is_returned, is_favorite, rating, is_read) VALUES (9, 13, 9, '2023-04-05', '2023-04-06', true, false, 3.20, true);
INSERT INTO public.borrowing (borrow_id, customer_id, book_id, borowing_date, return_date, is_returned, is_favorite, rating, is_read) VALUES (10, 13, 10, '2023-04-05', '2023-04-07', true, false, 2.00, true);
INSERT INTO public.borrowing (borrow_id, customer_id, book_id, borowing_date, return_date, is_returned, is_favorite, rating, is_read) VALUES (22, 13, 10, NULL, '2023-04-07', true, true, 2.00, true);
INSERT INTO public.borrowing (borrow_id, customer_id, book_id, borowing_date, return_date, is_returned, is_favorite, rating, is_read) VALUES (31, 13, 1, '2023-04-07', '2023-04-07', true, true, 5.00, true);


--
-- TOC entry 3346 (class 0 OID 17941)
-- Dependencies: 218
-- Data for Name: customer; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.customer (customer_id, first_name, last_name, phone, email, username, password, is_logined) VALUES (4, 'Daniel', '', NULL, NULL, 'dan', 'dan1', false);
INSERT INTO public.customer (customer_id, first_name, last_name, phone, email, username, password, is_logined) VALUES (6, 'Maurits', 'Escher', NULL, NULL, 'esher', 'esh1', false);
INSERT INTO public.customer (customer_id, first_name, last_name, phone, email, username, password, is_logined) VALUES (5, 'Vasiliy', 'Kandinskiy', NULL, NULL, 'kandinskiy', 'kand1', false);
INSERT INTO public.customer (customer_id, first_name, last_name, phone, email, username, password, is_logined) VALUES (13, 'Ammar', NULL, NULL, NULL, 'ammar', '123', true);


--
-- TOC entry 3356 (class 0 OID 0)
-- Dependencies: 215
-- Name: book_book_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.book_book_id_seq', 5, true);


--
-- TOC entry 3357 (class 0 OID 0)
-- Dependencies: 217
-- Name: borrowing_borrow_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.borrowing_borrow_id_seq', 31, true);


--
-- TOC entry 3358 (class 0 OID 0)
-- Dependencies: 219
-- Name: customer_customer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.customer_customer_id_seq', 16, true);


--
-- TOC entry 3193 (class 2606 OID 17950)
-- Name: book book_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book
    ADD CONSTRAINT book_pkey PRIMARY KEY (book_id);


--
-- TOC entry 3195 (class 2606 OID 17952)
-- Name: borrowing borrowing_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.borrowing
    ADD CONSTRAINT borrowing_pkey PRIMARY KEY (borrow_id);


--
-- TOC entry 3197 (class 2606 OID 17954)
-- Name: customer customer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_pkey PRIMARY KEY (customer_id);


--
-- TOC entry 3198 (class 2606 OID 17955)
-- Name: borrowing book; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.borrowing
    ADD CONSTRAINT book FOREIGN KEY (book_id) REFERENCES public.book(book_id) NOT VALID;


--
-- TOC entry 3199 (class 2606 OID 17960)
-- Name: borrowing customer; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.borrowing
    ADD CONSTRAINT customer FOREIGN KEY (customer_id) REFERENCES public.customer(customer_id) NOT VALID;


-- Completed on 2023-04-07 02:49:36

--
-- PostgreSQL database dump complete
--

