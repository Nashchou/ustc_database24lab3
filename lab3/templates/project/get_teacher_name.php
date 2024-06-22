<?php
header('Content-Type: application/json');

$servername = "localhost";
$username = "root"; // 修改为你的数据库用户名
$password = "20040501"; // 修改为你的数据库密码
$dbname = "lab3";

// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接
if ($conn->connect_error) {
    die(json_encode(['success' => false, 'message' => '数据库连接失败']));
}

if (isset($_GET['job_number'])) {
    $job_number = $conn->real_escape_string($_GET['job_number']);
    $sql = "SELECT name FROM teacher WHERE id = '$job_number'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        echo json_encode(['success' => true, 'name' => $row['name']]);
    } else {
        echo json_encode(['success' => false, 'message' => '未找到该工号对应的老师']);
    }
} else {
    echo json_encode(['success' => false, 'message' => '缺少参数']);
}

$conn->close();
?>
