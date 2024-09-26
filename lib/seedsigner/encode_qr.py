import math

from embit import bip32
from embit.networks import NETWORKS
from binascii import hexlify
from dataclasses import dataclass
from typing import List
from embit import bip32
from embit.networks import NETWORKS
from embit.psbt import PSBT
from seedsigner.helpers.ur2.ur_encoder import UREncoder
from seedsigner.helpers.ur2.ur import UR
from seedsigner.helpers.qr import QR
from seedsigner.models.seed import Seed
from seedsigner.models.settings import SettingsConstants

from urtypes.crypto import PSBT as UR_PSBT
from urtypes.crypto import Account, HDKey, Output, Keypath, PathComponent, SCRIPT_EXPRESSION_TAG_MAP



@dataclass
class BaseQrEncoder:
    qr_density: str = SettingsConstants.DENSITY__MEDIUM


    def __post_init__(self):
        self.qr = QR()


    @property
    def is_complete(self):
        raise Exception("Not implemented in child class")

    @property
    def qr_max_fragment_size(self):
        raise Exception("Not implemented in child class")

    def seq_len(self):
        raise Exception("Not implemented in child class")

    def next_part(self) -> str:
        raise Exception("Not implemented in child class")
    
    def cur_part(self) -> str:
        raise Exception("Not implemented in child class")
    
    def restart(self):
        # only used by animated QR encoders
        pass

    def _create_parts(self):
        raise Exception("Not implemented in child class")


    def part_to_image(self, part, width, height, border: int = 3, background_color: str = "ffffff"):
        return self.qr.qrimage_io(part, width, height, border, background_color=background_color)


    def next_part_image(self, width=240, height=240, border=3, background_color="bdbdbd"):
        part = self.next_part()
        return self.part_to_image(part, width, height, border, background_color=background_color)




"""**************************************************************************************
    STATIC QR encoders
**************************************************************************************"""
@dataclass
class BaseStaticQrEncoder(BaseQrEncoder):
    def seq_len(self):
        return 1
    
    def cur_part(self) -> str:
        """ static QRs only have a single part, which `next_part` always returns """
        return self.next_part()


    @property
    def is_complete(self):
        return True



@dataclass
class SeedQrEncoder(BaseStaticQrEncoder):
    mnemonic: List[str] = None
    wordlist_language_code: str = SettingsConstants.WORDLIST_LANGUAGE__ENGLISH


    def __post_init__(self):
        self.wordlist = Seed.get_wordlist(self.wordlist_language_code)
        super().__post_init__()

        self.data = ""
        # Output as Numeric data format
        for word in self.mnemonic:
            index = self.wordlist.index(word)
            self.data += str("%04d" % index)
    

    def next_part(self):
        return self.data



@dataclass
class CompactSeedQrEncoder(SeedQrEncoder):
    def next_part(self):
        # Output as binary data format
        binary_str = ""
        for word in self.mnemonic:
            index = self.wordlist.index(word)

            # Convert index to binary, strip out '0b' prefix; zero-pad to 11 bits
            binary_str += bin(index).split('b')[1].zfill(11)

        # We can exclude the checksum bits at the end
        if len(self.mnemonic) == 24:
            # 8 checksum bits in a 24-word seed
            binary_str = binary_str[:-8]

        elif len(self.mnemonic) == 12:
            # 4 checksum bits in a 12-word seed
            binary_str = binary_str[:-4]

        # Now convert to bytes, 8 bits at a time
        as_bytes = bytearray()
        for i in range(0, math.ceil(len(binary_str) / 8)):
            # int conversion reads byte data as a string prefixed with '0b'
            as_bytes.append(int('0b' + binary_str[i*8:(i+1)*8], 2))
        
        # Must return data as `bytes` for `qrcode` to properly recognize it as byte data
        return bytes(as_bytes)



@dataclass
class GenericStaticQrEncoder(BaseStaticQrEncoder):
    data: str = None

    def next_part(self):
        return self.data



@dataclass
class BaseXpubQrEncoder(BaseQrEncoder):
    """
    Base Xpub QrEncoder for static and animated formats
    """
    seed: Seed = None
    derivation: str = None
    network: str = SettingsConstants.MAINNET
    sig_type : str = None

    def prep_xpub(self):
            
        version = self.seed.detect_version(self.derivation, self.network, self.sig_type)
        self.root = bip32.HDKey.from_seed(self.seed.seed_bytes, version=NETWORKS[SettingsConstants.map_network_to_embit(self.network)]["xprv"])
        self.fingerprint = self.root.child(0).fingerprint
        self.xprv = self.root.derive(self.derivation)
        self.xpub = self.xprv.to_public()
        self.xpub_base58 = self.xpub.to_string(version=version)

        self.xpubstring = "[{}{}]{}".format(
            hexlify(self.fingerprint).decode('utf-8'),
            self.derivation[1:],
            self.xpub_base58
        )



class StaticXpubQrEncoder(BaseXpubQrEncoder, BaseStaticQrEncoder):
    def __post_init__(self):
        super().__post_init__()
        self.prep_xpub()


    def next_part(self):
        self.prep_xpub()
        return self.xpubstring



"""**************************************************************************************
    Simple animated QR encoders
**************************************************************************************"""
@dataclass
class BaseSimpleAnimatedQREncoder(BaseQrEncoder):
    def __post_init__(self):
        super().__post_init__()
        self.parts = []
        self.part_num_sent = 0
        self.sent_complete = False
        self._create_parts()


    @property
    def is_complete(self):
        return self.sent_complete


    def seq_len(self):
        return len(self.parts)


    def next_part(self) -> str:
        # if part num sent is gt number of parts, start at 0
        if self.part_num_sent > (len(self.parts) - 1):
            self.part_num_sent = 0

        part = self.parts[self.part_num_sent]

        # when parts sent eq num of parts in list
        if self.part_num_sent == (len(self.parts) - 1):
            self.sent_complete = True

        # increment to next part
        self.part_num_sent += 1

        return part


    def cur_part(self) -> str:
        if self.part_num_sent == 0:
            # Rewind all the way back to the end
            self.part_num_sent = len(self.parts) - 1
        else:
            self.part_num_sent -= 1
        return self.next_part()


    def restart(self) -> str:
        self.part_num_sent = 0



@dataclass
class SpecterXPubQrEncoder(BaseSimpleAnimatedQREncoder, BaseXpubQrEncoder):
    @property
    def qr_max_fragment_size(self):
        density_mapping = {
            SettingsConstants.DENSITY__LOW: 40,
            SettingsConstants.DENSITY__MEDIUM: 65,
            SettingsConstants.DENSITY__HIGH: 90,
        }
        return density_mapping.get(self.qr_density, 65)


    def _create_parts(self):
        self.prep_xpub()
        start = 0
        stop = self.qr_max_fragment_size
        qr_cnt = ((len(self.xpubstring)-1) // self.qr_max_fragment_size) + 1

        if qr_cnt == 1:
            self.parts.append(self.xpubstring[start:stop])

        cnt = 0
        while cnt < qr_cnt and qr_cnt != 1:
            part = "p" + str(cnt+1) + "of" + str(qr_cnt) + " " + self.xpubstring[start:stop]
            self.parts.append(part)

            start = start + self.qr_max_fragment_size
            stop = stop + self.qr_max_fragment_size
            if stop > len(self.xpubstring):
                stop = len(self.xpubstring)
            cnt += 1
