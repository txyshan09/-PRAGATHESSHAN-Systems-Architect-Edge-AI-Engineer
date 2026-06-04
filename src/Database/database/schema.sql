-- Matrix-School Enterprise Core Database Structure
-- Enforces clean data integrity and optimized query performance.

CREATE DATABASE IF NOT EXISTS `matrix_school_system` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `matrix_school_system`;

-- 1. ADMINISTRATORS TABLE (Manages high-level system users)
CREATE TABLE IF NOT EXISTS `administrators` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL, -- Never store raw passwords
    `full_name` VARCHAR(100) NOT NULL,
    `role` ENUM('SuperAdmin', 'Principal', 'DisciplineOfficer') NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 2. STUDENTS TABLE (Tracks core student enrollment parameters)
CREATE TABLE IF NOT EXISTS `students` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `student_uid` VARCHAR(20) NOT NULL UNIQUE, -- Custom school tracking ID
    `first_name` VARCHAR(50) NOT NULL,
    `last_name` VARCHAR(50) NOT NULL,
    `grade_level` INT NOT NULL,
    `status` ENUM('Active', 'Suspended', 'Expelled') DEFAULT 'Active',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 3. DISCIPLINARY LOGS TABLE (The high-density tracking registry)
CREATE TABLE IF NOT EXISTS `disciplinary_logs` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `student_id` INT NOT NULL,
    `reported_by` INT NOT NULL,
    `infraction_type` VARCHAR(100) NOT NULL, -- e.g., 'Tardiness', 'Academic Dishonesty'
    `severity_level` ENUM('Low', 'Medium', 'High', 'Critical') NOT NULL,
    `description` TEXT NOT NULL,
    `action_taken` VARCHAR(255) DEFAULT NULL,
    `logged_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Performance Indexing for fast high-density administrative searches
    INDEX `idx_student_search` (`student_id`),
    INDEX `idx_severity` (`severity_level`),
    
    -- Database Relational Rules (Deletes logs automatically if a student profile is purged)
    FOREIGN KEY (`student_id`) REFERENCES `students`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`reported_by`) REFERENCES `administrators`(`id`) ON DELETE RESTRICT
) ENGINE=InnoDB;
