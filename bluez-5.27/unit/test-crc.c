/*
 *
 *  BlueZ - Bluetooth protocol stack for Linux
 *
 *  Copyright (C) 2011  Intel Corporation
 *
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include "monitor/crc.h"

#include <glib.h>

struct crc_data {
	const void *packet;
	size_t size;
	uint32_t crc_init;
};

static const unsigned char packet_1[] = {
	0xd6, 0xbe, 0x89, 0x8e, 0x00, 0x17, 0x7e, 0x01,
	0x00, 0xd0, 0x22, 0x00, 0x02, 0x01, 0x06, 0x03,
	0x02, 0x0d, 0x18, 0x06, 0xff, 0x6b, 0x00, 0x03,
	0x16, 0x52, 0x02, 0x0a, 0x00, 0xf4, 0x09, 0x92,
};

static const struct crc_data crc_1 = {
	.packet = packet_1,
	.size = sizeof(packet_1),
};

static const unsigned char packet_2[] = {
	0xd6, 0xbe, 0x89, 0x8e, 0x00, 0x17, 0x7e, 0x01,
	0x00, 0xd0, 0x22, 0x00, 0x02, 0x01, 0x06, 0x03,
	0x02, 0x0d, 0x18, 0x06, 0xff, 0x6b, 0x00, 0x03,
	0x16, 0x54, 0x02, 0x0a, 0x00, 0x95, 0x5f, 0x14,
};

static const struct crc_data crc_2 = {
	.packet = packet_2,
	.size = sizeof(packet_2),
};

static const unsigned char packet_3[] = {
	0xd6, 0xbe, 0x89, 0x8e, 0x00, 0x17, 0x7e, 0x01,
	0x00, 0xd0, 0x22, 0x00, 0x02, 0x01, 0x06, 0x03,
	0x02, 0x0d, 0x18, 0x06, 0xff, 0x6b, 0x00, 0x03,
	0x16, 0x55, 0x02, 0x0a, 0x00, 0x85, 0x66, 0x63,
};

static const struct crc_data crc_3 = {
	.packet = packet_3,
	.size = sizeof(packet_3),
};

static const unsigned char packet_4[] = {
	0xd6, 0xbe, 0x89, 0x8e, 0x00, 0x17, 0x7e, 0x01,
	0x00, 0xd0, 0x22, 0x00, 0x02, 0x01, 0x06, 0x03,
	0x02, 0x0d, 0x18, 0x06, 0xff, 0x6b, 0x00, 0x03,
	0x16, 0x53, 0x02, 0x0a, 0x00, 0xe4, 0x30, 0xe5,
};

static const struct crc_data crc_4 = {
	.packet = packet_4,
	.size = sizeof(packet_4),
};

static const unsigned char packet_5[] = {
	0xd6, 0xbe, 0x89, 0x8e, 0x03, 0x0c, 0x46, 0x1c,
	0xda, 0x72, 0x02, 0x00, 0x7e, 0x01, 0x00, 0xd0,
	0x22, 0x00, 0x6e, 0xf4, 0x6f,
};

static const struct crc_data crc_5 = {
	.packet = packet_5,
	.size = sizeof(packet_5),
};

static const unsigned char packet_6[] = {
	0xd6, 0xbe, 0x89, 0x8e, 0x04, 0x17, 0x7e, 0x01,
	0x00, 0xd0, 0x22, 0x00, 0x10, 0x09, 0x50, 0x6f,
	0x6c, 0x61, 0x72, 0x20, 0x48, 0x37, 0x20, 0x30,
	0x30, 0x30, 0x31, 0x37, 0x45, 0x0f, 0x8a, 0x65,
};

static const struct crc_data crc_6 = {
	.packet = packet_6,
	.size = sizeof(packet_6),
};

static const unsigned char packet_7[] = {
	0xd6, 0xbe, 0x89, 0x8e, 0x05, 0x22, 0x46, 0x1c,
	0xda, 0x72, 0x02, 0x00, 0x7e, 0x01, 0x00, 0xd0,
	0x22, 0x00, 0x96, 0x83, 0x9a, 0xaf, 0xbe, 0x1d,
	0x16, 0x03, 0x05, 0x00, 0x36, 0x00, 0x00, 0x00,
	0x2a, 0x00, 0xff, 0xff, 0xff, 0xff, 0x1f, 0xa5,
	0x77, 0x2d, 0x95,
};

static const struct crc_data crc_7 = {
	.packet = packet_7,
	.size = sizeof(packet_7),
};

static const unsigned char packet_8[] = {
	0x96, 0x83, 0x9a, 0xaf, 0x01, 0x00, 0xc7, 0x15,
	0x4d,
};

static const struct crc_data crc_8 = {
	.packet = packet_8,
	.size = sizeof(packet_8),
	.crc_init = 0x161dbe,		/* from packet_7 = 0xbe 0x1d 0x16 */
};

static const unsigned char packet_9[] = {
	0x96, 0x83, 0x9a, 0xaf, 0x06, 0x14, 0x10, 0x00,
	0x04, 0x00, 0x09, 0x07, 0x10, 0x00, 0x10, 0x11,
	0x00, 0x37, 0x2a, 0x13, 0x00, 0x02, 0x14, 0x00,
	0x38, 0x2a, 0x73, 0x2a, 0xa3,
};

static const struct crc_data crc_9 = {
	.packet = packet_9,
	.size = sizeof(packet_9),
	.crc_init = 0x161dbe,		/* from packet_7 = 0xbe 0x1d 0x16 */
};

static void test_crc(gconstpointer data)
{
	const struct crc_data *test_data = data;
	const uint8_t *buf = test_data->packet + test_data->size - 3;
	uint32_t crc_init, crc_value, crc, rev;

	if (test_data->crc_init)
		crc_init = crc24_bit_reverse(test_data->crc_init);
	else
		crc_init = crc24_bit_reverse(0x555555);

	crc_value = buf[0] | buf[1] << 8 | buf[2] << 16;

	crc = crc24_calculate(crc_init, test_data->packet + 4,
						test_data->size - 7);

	if (g_test_verbose())
		g_print("CRC: 0x%6.6x, Calculated: 0x%6.6x\n",
						crc_value, crc);

	g_assert(crc_value == crc);

	rev = crc24_reverse(crc_value, test_data->packet + 4,
						test_data->size - 7);

	if (g_test_verbose())
		g_print("Preset: 0x%6.6x, Calculated: 0x%6.6x\n",
						crc_init, rev);

	g_assert(crc_init == rev);
}

int main(int argc, char *argv[])
{
	g_test_init(&argc, &argv, NULL);

	g_test_add_data_func("/crc/1", &crc_1, test_crc);
	g_test_add_data_func("/crc/2", &crc_2, test_crc);
	g_test_add_data_func("/crc/3", &crc_3, test_crc);
	g_test_add_data_func("/crc/4", &crc_4, test_crc);
	g_test_add_data_func("/crc/5", &crc_5, test_crc);
	g_test_add_data_func("/crc/6", &crc_6, test_crc);
	g_test_add_data_func("/crc/7", &crc_7, test_crc);
	g_test_add_data_func("/crc/8", &crc_8, test_crc);
	g_test_add_data_func("/crc/9", &crc_9, test_crc);

	return g_test_run();
}