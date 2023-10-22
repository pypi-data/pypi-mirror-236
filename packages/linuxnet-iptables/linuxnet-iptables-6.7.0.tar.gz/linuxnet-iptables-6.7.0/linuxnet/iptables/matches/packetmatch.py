# Copyright (c) 2021, 2022, 2023, Panagiotis Tsirigotis

# This file is part of linuxnet-iptables.
#
# linuxnet-iptables is free software: you can redistribute it and/or
# modify it under the terms of version 3 of the GNU Affero General Public
# License as published by the Free Software Foundation.
#
# linuxnet-iptables is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public
# License for more details.
#
# You should have received a copy of the GNU Affero General
# Public License along with linuxnet-iptables. If not, see
# <https://www.gnu.org/licenses/>.

"""
This module provides the PacketMatch class which supports
matching against standard packet attributes
"""

from ipaddress import IPv4Network
from typing import Iterable, List, Optional

from ..exceptions import IptablesError, IptablesParsingError
from ..deps import get_logger

from .match import Criterion, Match, MatchParser
from .util import BooleanCriterion, GenericCriterion

_logger = get_logger('linuxnet.iptables.matches.packetmatch')


class InputInterfaceCriterion(GenericCriterion):
    """Compare with the input interface.

    The comparison value is an interface name (a string).
    """
    def __init__(self, match: Match):
        super().__init__(match, '-i')


class OutputInterfaceCriterion(GenericCriterion):
    """Compare with the output interface.

    The comparison value is an interface name (a string).
    """
    def __init__(self, match: Match):
        super().__init__(match, '-o')


class SourceAddressCriterion(GenericCriterion):
    """Compare with the source address.

    The comparison value is an :class:`IPv4Network`.
    """
    def __init__(self, match: Match):
        super().__init__(match, '-s')


class DestAddressCriterion(GenericCriterion):
    """Compare with the destination address.

    The comparison value is an :class:`IPv4Network`.
    """
    def __init__(self, match: Match):
        super().__init__(match, '-d')


class ProtocolCriterion(Criterion):
    """Compare with the protocol.

    The comparison value is a protocol name (a string); it may also
    be a number in string form if there is no mapping of that number
    to a protocol name in ``/etc/protocols``.
    """

    # Key: protocol number
    # Value: protocol name
    __proto_map = {}
    __proto_map_ready = False

    def __init__(self, match: Match):
        super().__init__(match)
        self.__proto_name = None

    @classmethod
    def __getprotobynumber(cls, protonum: int) -> Optional[str]:
        """Returns the protocol name for the specified protocol
        """
        if cls.__proto_map_ready:
            return cls.__proto_map.get(protonum)
        try:
            with open("/etc/protocols", encoding="utf-8") as protofile:
                for line in protofile:
                    pos = line.find('#')
                    if pos < 0:
                        line = line.strip()
                    else:
                        line = line[:pos].strip()
                    if not line:
                        continue
                    fields = line.split()
                    if len(fields) < 2:
                        continue
                    try:
                        cls.__proto_map[int(fields[1])] = fields[0]
                    except ValueError:
                        pass
        except Exception:               # pylint: disable=broad-except
            _logger.exception("unable to process /etc/protocols")
        finally:
            cls.__proto_map_ready = True
        return cls.__proto_map.get(protonum)

    def get_value(self) -> str:
        """Return protocol name
        """
        return self.__proto_name

    def equals(self, proto) -> Match:   # pylint: disable=arguments-differ
        """Compare with the specified protocol.

        :param proto: the parameter can a string or an integer; if it
            is an integer, it will be converted to the corresponding
            protocol name, if possible, otherwise it will be used as-is
            in string form (i.e. 199 will be converted to "199")
        """
        if isinstance(proto, str):
            # Check if is a number in string form
            try:
                self.__proto_name = self.__getprotobynumber(int(proto)) or proto
            except ValueError:
                self.__proto_name = proto
        elif isinstance(proto, int):
            self.__proto_name = self.__getprotobynumber(int(proto)) or \
                                                str(proto)
        else:
            raise IptablesError(f'unexpected argument type: {proto}')
        return self._set_polarity(True)

    def _crit_iptables_args(self) -> List[str]:
        """Returns **iptables(8)** arguments for the specified protocol
        """
        return ['-p', self.__proto_name]


class FragmentCriterion(BooleanCriterion):
    """Check if a packet is a fragment.
    """

    def __init__(self, match: Match):
        super().__init__(match, '-f')


class PacketMatch(Match):
    """This class provides matching against the following attributes of
    a packet:

    * input interface
    * output interface
    * protocol
    * source address
    * destination address
    * fragment bit

    """

    def __init__(self):
        self.__iif_crit = None
        self.__oif_crit = None
        self.__proto_crit = None
        self.__frag_crit = None
        self.__source_crit = None
        self.__dest_crit = None

    @staticmethod
    def get_match_name() -> Optional[str]:
        """Returns the **iptables(8)** match extension name. In the case of
        the standard packet match, there is no name.
        """
        return None

    def get_criteria(self) -> Iterable['Criterion']:
        """Returns the packet match criteria: input-interface, output-interface,
        protocol, fragmented, source, destination.
        """
        return (
                            self.__iif_crit,
                            self.__oif_crit,
                            self.__proto_crit,
                            self.__frag_crit,
                            self.__source_crit,
                            self.__dest_crit,
                        )

    def protocol(self) -> ProtocolCriterion:
        """Match against the protocol
        """
        if self.__proto_crit is None:
            self.__proto_crit = ProtocolCriterion(self)
        return self.__proto_crit

    def input_interface(self) -> InputInterfaceCriterion:
        """Match against the input interface
        """
        if self.__iif_crit is None:
            self.__iif_crit = InputInterfaceCriterion(self)
        return self.__iif_crit

    def output_interface(self) -> OutputInterfaceCriterion:
        """Match against the output interface
        """
        if self.__oif_crit is None:
            self.__oif_crit = OutputInterfaceCriterion(self)
        return self.__oif_crit

    def source_address(self) -> SourceAddressCriterion:
        """Match against the source address
        """
        if self.__source_crit is None:
            self.__source_crit = SourceAddressCriterion(self)
        return self.__source_crit

    def dest_address(self) -> DestAddressCriterion:
        """Match against the destination address
        """
        if self.__dest_crit is None:
            self.__dest_crit = DestAddressCriterion(self)
        return self.__dest_crit

    def fragment(self) -> FragmentCriterion:
        """Match if packet has (or has not) the fragment bit set
        """
        if self.__frag_crit is None:
            self.__frag_crit = FragmentCriterion(self)
        return self.__frag_crit

    @classmethod
    def _parse(cls, field_iter) -> Optional['PacketMatch']:
        """Parse the following fields, which will be returned in-order
        from field_iter:
            protocol, options, input-interface, output-interface,
            source, destination
        Returns a :class:`PacketMatch` object if any criteria for the above
        fields are defined, otherwise ``None``

        :param field_iter: an iterator that returns the fields of an
            **iptables(8)** output line starting with the protocol field

        :meta private:
        """
        packet_match = PacketMatch()
        proto = next(field_iter)
        if proto != 'all':
            is_equal, proto = MatchParser.parse_value(proto)
            packet_match.protocol().compare(is_equal, proto)
        opt = next(field_iter)
        if opt == '--':
            pass
        elif opt == '-f':
            packet_match.fragment().equals()
        elif opt == '!f':
            packet_match.fragment().not_equals()
        else:
            raise IptablesParsingError(f'cannot parse option: {opt}')
        iif = next(field_iter)
        if iif != '*':
            is_equal, interface_name = MatchParser.parse_value(iif)
            packet_match.input_interface().compare(is_equal, interface_name)
        oif = next(field_iter)
        if oif != '*':
            is_equal, interface_name = MatchParser.parse_value(oif)
            packet_match.output_interface().compare(is_equal, interface_name)
        source = next(field_iter)
        if source != '0.0.0.0/0':
            is_equal, addr = MatchParser.parse_value(source)
            packet_match.source_address().compare(is_equal, IPv4Network(addr))
        dest = next(field_iter)
        if dest != '0.0.0.0/0':
            is_equal, addr = MatchParser.parse_value(dest)
            packet_match.dest_address().compare(is_equal, IPv4Network(addr))
        return packet_match if packet_match.has_criteria() else None
