# Generated by Django 3.0.7 on 2020-07-30 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generate', '0002_auto_20200730_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='lookup_id',
            field=models.CharField(choices=[('1', 'point'), ('2', 'sensor point'), ('3', 'cmd point'), ('4', 'sp point'), ('5', 'param point'), ('6', 'temp sensor point'), ('7', 'air temp sensor point'), ('8', 'discharge air temp sensor point'), ('9', 'return air temp sensor point'), ('10', 'exhaust air temp sensor point'), ('11', 'mixed air temp sensor point'), ('12', 'run cmd point'), ('13', 'stage:1 cmd point'), ('14', 'stage:2 cmd point'), ('15', 'humidity sensor point'), ('16', 'air humidity sensor point'), ('17', 'return air humidity sensor point'), ('18', 'outside air humidity sensor point'), ('19', 'mixed air humidity sensor point'), ('20', 'zone air temp sensor point'), ('21', 'zone air humidity sensor point'), ('22', 'temp sp point'), ('23', 'air temp sp point'), ('24', 'zone air temp sp point'), ('25', 'humidity sp point'), ('26', 'air humidity sp point'), ('27', 'zone air humidity sp point'), ('28', 'mixed air temp sp point'), ('29', 'discharge air temp sp point'), ('30', 'outside air temp sensor point'), ('31', 'damper cmd point'), ('32', 'outside damper cmd point'), ('33', 'fan run cmd point'), ('34', 'discharge fan run cmd point'), ('35', 'flow sensor point'), ('36', 'air flow sensor point'), ('37', 'enable cmd point'), ('38', 'status point'), ('39', 'position cmd point'), ('40', 'modulating damper cmd point'), ('41', 'twoPosition damper cmd point'), ('42', 'valve cmd point'), ('43', 'modulating valve cmd point'), ('44', 'twoPosition valve cmd point'), ('45', 'damper sensor point'), ('46', 'valve sensor point'), ('47', 'discharge air flow sensor point'), ('48', 'mixed air flow sensor point'), ('49', 'exhaust air flow sensor point'), ('50', 'outside air flow sensor point'), ('51', 'return air flow sensor point'), ('52', 'twoPosition cmd point'), ('53', 'modulating cmd point'), ('54', 'cooling zone air temp sp point'), ('55', 'occ cooling zone air temp sp point'), ('56', 'unocc cooling zone air temp sp point'), ('57', 'standby cooling zone air temp sp point'), ('58', 'heating zone air temp sp point'), ('59', 'occ heating zone air temp sp point'), ('60', 'unocc heating zone air temp sp point'), ('61', 'standby heating zone air temp sp point'), ('62', 'stage:N cmd point'), ('63', 'modulating position cmd point'), ('64', 'pressure sensor point'), ('65', 'air pressure sensor point'), ('66', 'discharge air pressure sensor point'), ('67', 'return air pressure sensor point'), ('68', 'speed cmd point'), ('69', 'run sensor point'), ('70', float("nan"))], max_length=100),
        ),
    ]
