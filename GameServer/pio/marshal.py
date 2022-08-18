# -*- coding: utf-8 -*-

class MarshalException(Exception):
    pass


class Marshal:
    def marshal(self, osstream):
        assert 0, 'abstract method Marshal::marshal'

    def unmarshal(self, osstream):
        assert 0, 'abstract method Marshal::unmarshal'
