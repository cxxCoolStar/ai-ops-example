import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def process_data(data):
    """Process the data and return an integer result."""
    try:
        return int(data)
    except (ValueError, TypeError) as e:
        logging.warning(f"Invalid data format: {data!r}, skipping...")
        return None

def main():
    logging.info("服务已启动 - v1.0.0")
    logging.info("初始化组件成功")
    
    # Sample data processing
    data_items = [100, 200, "abc", 300]
    
    for item in data_items:
        logging.info(f"开始处理项目: {item}")
        logging.debug(f"正在处理数据: {item}")
        
        result = process_data(item)
        
        if result is not None:
            logging.info(f"项目处理成功: {item} -> {result}")
        else:
            logging.warning(f"项目处理失败: {item}")
    
    logging.info("所有项目处理完成")

if __name__ == "__main__":
    main()