from tile_world.tile_world_writer.file_helpers import *
from tile_world.tile_world_level import TileWorldLevel
from tile_world.tile_world_tiles import monster_tiles

import numpy as np

class PositionWriter:
    @staticmethod
    def write(data, position, size=WORD_SIZE):
        wb(data, position[1], size)
        wb(data, position[0], size)



class ButtonObjectConnectionWriter:
    @staticmethod
    def write(data, connection):
        PositionWriter.write(data, connection.button_position)
        PositionWriter.write(data, connection.object_position)


class Field:
    def __init__(self):
        self.field_type = 0x00
        

    def write(self, data):
        wb(data, self.field_type, BYTE_SIZE)
        additional_bytes_field_placeholder = placeholder(data, BYTE_SIZE)
        self.write_field_data(data)
        fill_placeholder(data, additional_bytes_field_placeholder)
    

    def write_field_data(self, data):
        pass



class TitleField(Field):
    def __init__(self, map_title):
        self.map_title = map_title
        self.field_type = 0x03
    

    def write_field_data(self, data):
        map_title_bytes = self.map_title.encode(encoding='ascii')
        for byte in map_title_bytes:
            data.append(byte)
        wb(data, 0, BYTE_SIZE) # Magic number 0



class HintField(TitleField):
    def __init__(self, map_hint):
        self.map_title = map_hint
        self.field_type = 0x07



class PasswordField(Field):
    def __init__(self, map_password):
        self.map_password = map_password
        self.field_type = 0x06


    def encrypt_password(self, password):
        password_xor = 0x99
        encrypted_password = []
        for character in password:
            encrypted_password.append(ord(character.encode('ascii')) ^ password_xor)
        return encrypted_password
    

    def write_field_data(self, data):
        encrypted_password = self.encrypt_password(self.map_password)
        for byte in encrypted_password:
            data.append(byte)
        wb(data, 0, BYTE_SIZE) # Magic number 0



class TrapsField(Field):
    def __init__(self, traps):
        self.field_type = 0x04
        self.traps = traps
    

    def write_field_data(self, data):
        for trap in self.traps:
            ButtonObjectConnectionWriter.write(data, trap)
            wb(data, 0, WORD_SIZE) # Magic number 0



class ClonersField(Field):
    def __init__(self, cloners):
        self.field_type = 0x05
        self.cloners = cloners
    

    def write_field_data(self, data):
        for cloner in self.cloners:
            ButtonObjectConnectionWriter.write(data, cloner)



class MonstersField(Field):
    def __init__(self, upper_layer, lower_layer):
        self.field_type = 0x0A
        self.monster_positions = self.extract_monster_positions(upper_layer)
        self.monster_positions.extend(self.extract_monster_positions(lower_layer))

    def extract_monster_positions(self, layer):
        monster_positions = []
        for i, tile in enumerate(layer):
            if tile in monster_tiles:
                y = i // TileWorldLevel.LAYER_WIDTH
                x = i - TileWorldLevel.LAYER_WIDTH * y
                monster_positions.append(np.array([y, x]))
        return monster_positions

    

    def write_field_data(self, data):
        for monster_position in self.monster_positions:
            PositionWriter.write(data, monster_position, BYTE_SIZE)

