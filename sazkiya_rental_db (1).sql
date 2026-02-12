-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 12 Feb 2026 pada 15.08
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sazkiya_rental_db`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `mobil`
--

CREATE TABLE `mobil` (
  `id` int(11) NOT NULL,
  `nama_mobil` varchar(100) DEFAULT NULL,
  `harga` int(11) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `gambar` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `mobil_sazkiya`
--

CREATE TABLE `mobil_sazkiya` (
  `id` int(11) NOT NULL,
  `nama_mobil` varchar(100) DEFAULT NULL,
  `harga` int(11) DEFAULT NULL,
  `gambar` varchar(100) DEFAULT NULL,
  `status` enum('Tersedia','Disewa','maintenance') DEFAULT 'Tersedia',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `mobil_sazkiya`
--

INSERT INTO `mobil_sazkiya` (`id`, `nama_mobil`, `harga`, `gambar`, `status`, `created_at`) VALUES
(1, 'Pajero Sport 2022', 500000, 'pajero2022.png', 'Tersedia', '2026-02-11 02:47:40'),
(2, 'Lamborghini Huracan Evo', 1750000, 'lambohuracanevo.png', 'Disewa', '2026-02-11 02:47:40'),
(3, 'Innova Zenix', 600000, 'innovazenix.png', 'Tersedia', '2026-02-11 02:47:40'),
(4, 'Fortuner Facelift ', 1500000, 'fortunerfacelift.png', 'Disewa', '2026-02-11 02:47:40'),
(6, 'Xpander Mpv', 600000, 'xpandermpv.png', 'Tersedia', '2026-02-11 03:31:25'),
(7, 'Honda HR-V', 700000, 'hondahrv.png', 'Disewa', '2026-02-11 09:56:39'),
(8, 'Toyota Raize Hybrid Z', 350000, 'ToyotaRaizeHybridZ.png', 'Disewa', '2026-02-11 10:02:58');

-- --------------------------------------------------------

--
-- Struktur dari tabel `motor_sazkiya`
--

CREATE TABLE `motor_sazkiya` (
  `id` int(11) NOT NULL,
  `nama_motor` varchar(100) DEFAULT NULL,
  `harga` int(11) DEFAULT NULL,
  `gambar` varchar(100) DEFAULT NULL,
  `status` enum('tersedia','disewa','maintenance') DEFAULT 'tersedia'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `penyewaan_sazkiya`
--

CREATE TABLE `penyewaan_sazkiya` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `kendaraan_id` int(11) DEFAULT NULL,
  `jenis_kendaraan` enum('mobil','motor') DEFAULT NULL,
  `tanggal_sewa` date DEFAULT NULL,
  `tanggal_kembali` date DEFAULT NULL,
  `status` enum('aktif','selesai') DEFAULT 'aktif'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `users_sazkiya`
--

CREATE TABLE `users_sazkiya` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` enum('admin','user') DEFAULT 'user',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `users_sazkiya`
--

INSERT INTO `users_sazkiya` (`id`, `nama`, `email`, `password`, `role`, `created_at`) VALUES
(1, 'Admin', 'admin@gmail.com', 'HASH_PASSWORD', 'admin', '2026-02-11 02:47:40');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `mobil`
--
ALTER TABLE `mobil`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `mobil_sazkiya`
--
ALTER TABLE `mobil_sazkiya`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `motor_sazkiya`
--
ALTER TABLE `motor_sazkiya`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `penyewaan_sazkiya`
--
ALTER TABLE `penyewaan_sazkiya`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `users_sazkiya`
--
ALTER TABLE `users_sazkiya`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `mobil`
--
ALTER TABLE `mobil`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `mobil_sazkiya`
--
ALTER TABLE `mobil_sazkiya`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT untuk tabel `motor_sazkiya`
--
ALTER TABLE `motor_sazkiya`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `penyewaan_sazkiya`
--
ALTER TABLE `penyewaan_sazkiya`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `users_sazkiya`
--
ALTER TABLE `users_sazkiya`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
