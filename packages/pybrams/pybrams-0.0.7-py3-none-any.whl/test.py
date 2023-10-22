from brams import enable_cache, disable_cache, clear_cache
from brams import files
import json

enable_cache()
print("clearing cache")
# clearing cache
clear_cache()

print("downloading and caching")
# caching the file after downloading it
file = files.get("2023-01-01T00:00", "BEBILZ_SYS001")
file.load()


print("getting file out of the cache")
# getting file out of cache
cached_file = files.get("2023-01-01T00:00", "BEBILZ_SYS001")
cached_file.load()

print("disabling cache")
# disabling cache
disable_cache()

print("downloading the file")
# downloading the file
downloaded_file = files.get("2023-01-01T00:00", "BEBILZ_SYS001")

print("loading files")
# loading files
downloaded_file.load()
print("signal : ", (cached_file.signal.data == downloaded_file.signal.data).all())

print("comparing files")
# comparing files
print("cached_file == downloaded_file :", cached_file == downloaded_file)
print("cached_file.signal == downloaded_file.signal :", cached_file.signal == downloaded_file.signal)


print("beacon_freq : ", cached_file.signal.beacon_frequency == downloaded_file.signal.beacon_frequency)
print("signal : ", (cached_file.signal.data == downloaded_file.signal.data).all())
print("sample_rate : ", cached_file.signal.samplerate == downloaded_file.signal.samplerate)
print("nfft : ", cached_file.signal.nfft == downloaded_file.signal.nfft)
print("fft : ", (cached_file.signal.fft == downloaded_file.signal.fft).all())
print("real_fft_freq : ", (cached_file.signal.real_fft_freq == downloaded_file.signal.real_fft_freq).all())
print("real_fft : ", (cached_file.signal.real_fft == downloaded_file.signal.real_fft).all())





