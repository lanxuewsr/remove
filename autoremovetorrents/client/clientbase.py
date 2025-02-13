import time
from .. import logger

def remove_torrents(self, torrent_hash_list, remove_data):
    """
    Remove a list of torrents safely
    Parameters:
        torrent_hash_list - List of torrent hashes
        remove_data - Boolean, whether to remove data
    Returns:
        (success_list, failed_list) - Returns removed torrents and failed torrents with reasons
    """
    success_list = []
    failed_list = []
    
    try:
        # 获取logger
        self._logger = logger.Logger.register(__name__)
        
        for torrent_hash in torrent_hash_list:
            try:
                # 1. 暂停种子
                self._logger.info(f"Pausing torrent {torrent_hash}")
                self.pause_torrents([torrent_hash])
                
                # 2. 强制更新tracker
                self._logger.info(f"Forcing reannounce for torrent {torrent_hash}")
                self.force_reannounce([torrent_hash])
                
                # 3. 等待数据同步 (30秒)
                self._logger.info(f"Waiting for tracker update for torrent {torrent_hash}")
                time.sleep(30)
                
                # 4. 删除种子
                self._logger.info(f"Removing torrent {torrent_hash}")
                self._remove_torrent(torrent_hash, remove_data)
                
                success_list.append(torrent_hash)
                self._logger.info(f"Successfully removed torrent {torrent_hash}")
                
            except Exception as e:
                failed_list.append({
                    'hash': torrent_hash,
                    'reason': str(e)
                })
                self._logger.error(f"Failed to remove torrent {torrent_hash}: {str(e)}")
                
    except Exception as e:
        self._logger.error(f"Global error in remove_torrents: {str(e)}")
        
    return (success_list, failed_list)

def pause_torrents(self, torrent_hash_list):
    """
    Pause a list of torrents
    Parameters:
        torrent_hash_list - List of torrent hashes
    Raises:
        NotImplementedError - If not implemented in client
    """
    raise NotImplementedError("Implement this method in sub-class.")

def force_reannounce(self, torrent_hash_list):
    """
    Force reannounce torrents to tracker
    Parameters:
        torrent_hash_list - List of torrent hashes
    Raises:
        NotImplementedError - If not implemented in client
    """
    raise NotImplementedError("Implement this method in sub-class.")

def _remove_torrent(self, torrent_hash, remove_data):
    """
    Internal method to remove a single torrent
    Parameters:
        torrent_hash - Hash of the torrent
        remove_data - Whether to remove data
    Raises:
        NotImplementedError - If not implemented in client
    """
    raise NotImplementedError("Implement this method in sub-class.") 