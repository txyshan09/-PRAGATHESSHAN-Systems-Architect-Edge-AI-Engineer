<?php

namespace MatrixSchool\Database;

use \PDO;
use \PDOException;
use \RuntimeException;

/**
 * Class Connection
 * Core system engine to manage secure data streams for the school system.
 */
class Connection 
{
    private static ?PDO $instance = null;
    private PDO $connection;

    private function __construct() 
    {
        // Production-ready environment variables fallback
        $host     = $_ENV['DB_HOST'] ?? '127.0.0.1';
        $database = $_ENV['DB_NAME'] ?? 'matrix_school_system';
        $username = $_ENV['DB_USER'] ?? 'root';
        $password = $_ENV['DB_PASS'] ?? '';
        $port     = $_ENV['DB_PORT'] ?? '3306';
        
        $dsn = "mysql:host=$host;dbname=$database;port=$port;charset=utf8mb4";

        $options = [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES   => false, // Bulletproof protection against SQL injections
            PDO::ATTR_PERSISTENT         => true,  // Boosts system speed
        ];

        try {
            $this->connection = new PDO($dsn, $username, $password, $options);
        } catch (PDOException $e) {
            throw new RuntimeException("Database Connection Error: Fail-Safe Activated.");
        }
    }

    /**
     * Gets the active database connection anywhere in the project
     */
    public static function getInstance(): PDO 
    {
        if (self::$instance === null) {
            self::$instance = (new self())->connection;
        }
        return self::$instance;
    }

    // Safety mechanisms to prevent code breaking
    public function __clone() { throw new RuntimeException("Cloning prohibited."); }
    public function __wakeup() { throw new RuntimeException("Deserialization prohibited."); }
}
