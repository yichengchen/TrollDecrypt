

#import <Foundation/Foundation.h>
#import <mach/mach.h>
#import <mach-o/loader.h>
#import <mach-o/dyld_images.h>

typedef struct MainImageInfo {
    uint64_t loadAddress;     // main executable Mach-O header address
    NSString *path;           // main executable path
    BOOL     ok;
} MainImageInfo_t;

// Whether a Mach-O on disk still carries a live LC_ENCRYPTION_INFO command.
// TDEncryptionStateUnknown means the file could not be classified (fat binary,
// unreadable, ...) and the caller should fall back to inspecting the process.
typedef NS_ENUM(NSInteger, TDEncryptionState) {
    TDEncryptionStateUnknown = -1,
    TDEncryptionStateDecrypted,
    TDEncryptionStateEncrypted
};

NSString *NSStringFromMainImageInfo(MainImageInfo_t info);

TDEncryptionState encryptionStateOfImageAtPath(NSString *path);

MainImageInfo_t imageInfoForPIDWithRetry(const char *sourcePath, vm_map_t task, pid_t pid);

NSData *readLoadedImageHeader(vm_map_t task, uint64_t address);

@class TDMachOImage;
BOOL rebuildDecryptedImageAtPath(NSString *sourcePath, vm_map_t task,
                                 uint64_t loadAddress, TDMachOImage *image,
                                 NSString *outputPath, NSError **error);
