# coding=utf-8
import json
from ext.logic import CompanyExt
from core.model import db, bunny_engine as engine

__author__ = 'GaoJie'

# bind_key 用于绑定到对应的DATABASE
#__bind_key__ = 'users'


class Company(db.Model):
    __tablename__ = 'b_company'
    __table_args__ = {'autoload': True, 'autoload_with': engine}

    id = db.Column(db.Integer, primary_key=True)


class Campaign(db.Model):
    __tablename__ = 'b_campaign'
    __table_args__ = {'autoload': True, 'autoload_with': engine}

    id = db.Column(db.Integer, primary_key=True)
    companyId = db.Column(db.Integer, db.ForeignKey(Company.id))
    company = db.relationship(Company, primaryjoin=companyId == Company.id)


class CampaignAdgroup(db.Model):
    __tablename__ = 'b_campaign_adgroup'
    __table_args__ = {'autoload': True, 'autoload_with': engine}

    id = db.Column(db.Integer, primary_key=True)
    companyId = db.Column(db.Integer, db.ForeignKey(Company.id))
    company = db.relationship(Company, primaryjoin=companyId == Company.id)
    campaignId = db.Column(db.Integer, db.ForeignKey(Campaign.id))
    campaign = db.relationship(Campaign, primaryjoin=campaignId == Campaign.id)


class CampaignCreative(db.Model):
    __tablename__ = 'b_campaign_creative'
    __table_args__ = {'autoload': True, 'autoload_with': engine}

    id = db.Column(db.Integer, primary_key=True)
    companyId = db.Column(db.Integer, db.ForeignKey(Company.id))
    company = db.relationship(Company, primaryjoin=companyId == Company.id)
    campaignId = db.Column(db.Integer, db.ForeignKey(Campaign.id))
    campaign = db.relationship(Campaign, primaryjoin=campaignId == Campaign.id)
    adgroupId = db.Column(db.Integer, db.ForeignKey(CampaignAdgroup.id))
    adgroup = db.relationship(CampaignAdgroup, primaryjoin=adgroupId == CampaignAdgroup.id)

    #adx = db.relationship(CreativeAdx, lazy='joined')

    def get_format_template(self):
        return json.loads(self.adFormatTemplate)

    def set_format_template(self, object_dict):
        self.adFormatTemplate = json.dumps(object_dict)

    def file_source(self):
        """
        简单的通过creative获取投放物料的合理url
        :param creative:
        :return:
        """
        format_template = self.get_format_template()
        template = format_template['template']
        if self.creativeType in [1, 6]:
            file_source = template['adObject']['img_url']
        elif self.creativeType == 3:
            file_source = template['adObject']['video_url']
        elif self.creativeType == 2:
            file_source = template['adObject']['icon_url']
        else:
            return False
        return CompanyExt.attach_url(file_source, self.companyId)


class CreativeAdx(db.Model):
    __tablename__ = 'b_creative_adx'
    __table_args__ = {'autoload': True, 'autoload_with': engine}

    creativeId = db.Column(db.Integer, db.ForeignKey(CampaignCreative.id))
    adxId = db.Column(db.Integer)
    creative = db.relationship(CampaignCreative, primaryjoin=creativeId == CampaignCreative.id)
