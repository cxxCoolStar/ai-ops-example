import logging
import time


logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8",
)


def process_data(data):
    logging.debug(f"正在处理数据: {data}")
    try:
        return int(data)
    except ValueError as e:
        logging.warning(f"无法将 '{data}' 转换为整数: {e}")
        return None


def main():
    logging.info("服务已启动 - v1.0.0")
    print("服务已启动，正在运行...")

    time.sleep(1)
    logging.info("初始化组件成功")

    try:
        items = ["100", "200", "abc", "300"]
        for item in items:
            logging.info(f"开始处理项目: {item}")
            time.sleep(1)
            result = process_data(item)
            if result is not None:
                logging.info(f"项目处理成功: {result}")
            else:
                logging.info(f"项目跳过: {item} (无效数据)")
    except Exception as e:
        logging.error("处理过程中发生严重错误", exc_info=True)
        print(f"发生错误: {e}")


if __name__ == "__main__":
    main()