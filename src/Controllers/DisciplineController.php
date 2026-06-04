<?php

namespace MatrixSchool\Controllers;

use \PDO;
use MatrixSchool\Database\Connection;
use MatrixSchool\Authentication\AuthController;

/**
 * Class DisciplineController
 * Architected to execute high-density Create, Read, Update, Delete (CRUD)
 * operations on tracking data matrices while protecting database constraints.
 */
class DisciplineController 
{
    private PDO $db;

    public function __construct() 
    {
        // Enforce security authorization checkpoint before granting class interaction
        AuthController::checkGuard();
        $this->db = Connection::getInstance();
    }

    /**
     * Commits a new disciplinary tracking record into the database matrix.
     */
    public function logInfraction(int $studentId, int $adminId, string $type, string $severity, string $desc): bool 
    {
        $sql = "INSERT INTO disciplinary_logs (student_id, reported_by, infraction_type, severity_level, description) 
                VALUES (:student_id, :reported_by, :infraction_type, :severity_level, :description)";
        
        $stmt = $this->db->prepare($sql);
        
        return $stmt->execute([
            ':student_id'      => $studentId,
            ':reported_by'     => $adminId,
            ':infraction_type' => trim(filter_var($type, FILTER_SANITIZE_SPECIAL_CHARS)),
            ':severity_level'  => $severity, // Enforced by database ENUM options
            ':description'     => trim(filter_var($desc, FILTER_SANITIZE_SPECIAL_CHARS))
        ]);
    }

    /**
     * Fetches high-density tracking analytics filtered by student context.
     */
    public function getStudentHistory(int $studentId): array 
    {
        $sql = "SELECT d.*, a.full_name as officer_name 
                FROM disciplinary_logs d
                JOIN administrators a ON d.reported_by = a.id
                WHERE d.student_id = :student_id
                ORDER BY d.logged_at DESC";
                
        $stmt = $this->db->prepare($sql);
        $stmt->execute([':student_id' => $studentId]);
        
        return $stmt->fetchAll();
    }

    /**
     * Resolves a logged infraction node with administrative actions.
     */
    public function resolveInfraction(int $logId, string $actionTaken): bool 
    {
        $sql = "UPDATE disciplinary_logs 
                SET action_taken = :action_taken 
                WHERE id = :id";
                
        $stmt = $this->db->prepare($sql);
        
        return $stmt->execute([
            ':id'           => $logId,
            ':action_taken' => trim(filter_var($actionTaken, FILTER_SANITIZE_SPECIAL_CHARS))
        ]);
    }
}
