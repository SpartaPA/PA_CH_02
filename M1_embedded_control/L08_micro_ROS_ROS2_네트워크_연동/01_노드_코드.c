// [CH2 Physical AI] 8강. [실습] micro-ROS ROS2 네트워크 연동
// 절: 2-3. 노드 코드
// ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

/* 50Hz 타이머 콜백: 상태 퍼블리시 */
void state_timer_cb(rcl_timer_t *timer, int64_t last_call)
{
    state_msg.data.data[0] = g_speed_rpm;      // 7강의 volatile 변수들
    state_msg.data.data[1] = g_duty;
    rcl_publish(&state_pub, &state_msg, NULL);
}

/* 구독 콜백: 목표 속도 갱신 */
void target_cb(const void *msgin)
{
    const std_msgs__msg__Float32 *m = (const std_msgs__msg__Float32 *)msgin;
    g_target_rpm = m->data;                    // ISR의 PID가 다음 주기에 반영
}

void microros_task(void)
{
    // 초기화: support → node → pub/sub/timer → executor
    rclc_support_init(&support, 0, NULL, &allocator);
    rclc_node_init_default(&node, "motor_controller", "", &support);
    rclc_publisher_init_default(&state_pub, &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float32MultiArray), "motor/state");
    rclc_subscription_init_default(&target_sub, &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float32), "motor/target");
    rclc_timer_init_default(&state_timer, &support, RCL_MS_TO_NS(20), state_timer_cb);

    rclc_executor_init(&executor, &support.context, 2, &allocator);
    rclc_executor_add_timer(&executor, &state_timer);
    rclc_executor_add_subscription(&executor, &target_sub, &target_msg, target_cb, ON_NEW_DATA);

    while (1)
        rclc_executor_spin_some(&executor, RCL_MS_TO_NS(10));   // 메인 루프 = spin
}
