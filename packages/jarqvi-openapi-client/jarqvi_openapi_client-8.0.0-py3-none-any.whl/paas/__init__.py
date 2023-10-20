import os
import sys

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f'{path}')

import paas.openapi_client

# import apis into sdk package
from paas.openapi_client.api.apps_api import AppsApi
from paas.openapi_client.api.deploy_api import DeployApi
from paas.openapi_client.api.disks_api import DisksApi
from paas.openapi_client.api.domains_api import DomainsApi
from paas.openapi_client.api.reports_api import ReportsApi
from paas.openapi_client.api.settings_api import SettingsApi

# import ApiClient
from paas.openapi_client.api_response import ApiResponse
from paas.openapi_client.api_client import ApiClient
from paas.openapi_client.configuration import Configuration
from paas.openapi_client.exceptions import OpenApiException
from paas.openapi_client.exceptions import ApiTypeError
from paas.openapi_client.exceptions import ApiValueError
from paas.openapi_client.exceptions import ApiKeyError
from paas.openapi_client.exceptions import ApiAttributeError
from paas.openapi_client.exceptions import ApiException

# import models into sdk package
from paas.openapi_client.models.applets import Applets
from paas.openapi_client.models.applets_applets_inner import AppletsAppletsInner
from paas.openapi_client.models.applets_applets_inner_release import AppletsAppletsInnerRelease
from paas.openapi_client.models.change_plan_request import ChangePlanRequest
from paas.openapi_client.models.check_domain import CheckDomain
from paas.openapi_client.models.check_domain_domain import CheckDomainDomain
from paas.openapi_client.models.check_domain_domain_project import CheckDomainDomainProject
from paas.openapi_client.models.create_app import CreateApp
from paas.openapi_client.models.create_app_domain201_response import CreateAppDomain201Response
from paas.openapi_client.models.create_app_domain201_response_domain import CreateAppDomain201ResponseDomain
from paas.openapi_client.models.create_app_domain_request import CreateAppDomainRequest
from paas.openapi_client.models.create_disk_request import CreateDiskRequest
from paas.openapi_client.models.create_ftp200_response import CreateFtp200Response
from paas.openapi_client.models.create_ftp_request import CreateFtpRequest
from paas.openapi_client.models.deploy_releases import DeployReleases
from paas.openapi_client.models.domains import Domains
from paas.openapi_client.models.domains_domains_inner import DomainsDomainsInner
from paas.openapi_client.models.domains_domains_inner_project import DomainsDomainsInnerProject
from paas.openapi_client.models.download_backup200_response import DownloadBackup200Response
from paas.openapi_client.models.enable_ssl200_response import EnableSsl200Response
from paas.openapi_client.models.enable_ssl_request import EnableSslRequest
from paas.openapi_client.models.get_app_summary_reports200_response import GetAppSummaryReports200Response
from paas.openapi_client.models.get_app_summary_reports200_response_cpu_usage_inner import GetAppSummaryReports200ResponseCpuUsageInner
from paas.openapi_client.models.get_app_summary_reports200_response_cpu_usage_inner_value_inner import GetAppSummaryReports200ResponseCpuUsageInnerValueInner
from paas.openapi_client.models.get_app_summary_reports200_response_disks_usage_inner import GetAppSummaryReports200ResponseDisksUsageInner
from paas.openapi_client.models.get_disk_backup import GetDiskBackup
from paas.openapi_client.models.get_disk_backup_backups_inner import GetDiskBackupBackupsInner
from paas.openapi_client.models.get_disks import GetDisks
from paas.openapi_client.models.get_disks_disks_inner import GetDisksDisksInner
from paas.openapi_client.models.get_disks_mounts_inner import GetDisksMountsInner
from paas.openapi_client.models.get_ftps200_response import GetFtps200Response
from paas.openapi_client.models.get_ftps200_response_accesses_inner import GetFtps200ResponseAccessesInner
from paas.openapi_client.models.ip_static200_response import IpStatic200Response
from paas.openapi_client.models.logs_inner import LogsInner
from paas.openapi_client.models.project_all_details import ProjectAllDetails
from paas.openapi_client.models.project_all_details_project import ProjectAllDetailsProject
from paas.openapi_client.models.project_all_details_project_envs_inner import ProjectAllDetailsProjectEnvsInner
from paas.openapi_client.models.project_all_details_project_node import ProjectAllDetailsProjectNode
from paas.openapi_client.models.projects import Projects
from paas.openapi_client.models.projects_projects_inner import ProjectsProjectsInner
from paas.openapi_client.models.redirect_domain_request import RedirectDomainRequest
from paas.openapi_client.models.releases import Releases
from paas.openapi_client.models.releases_deploy200_response import ReleasesDeploy200Response
from paas.openapi_client.models.releases_releases_inner import ReleasesReleasesInner
from paas.openapi_client.models.releases_releases_inner_git_info import ReleasesReleasesInnerGitInfo
from paas.openapi_client.models.releases_releases_inner_git_info_author import ReleasesReleasesInnerGitInfoAuthor
from paas.openapi_client.models.reports import Reports
from paas.openapi_client.models.reports_result_inner import ReportsResultInner
from paas.openapi_client.models.resize_disk_request import ResizeDiskRequest
from paas.openapi_client.models.set_app_domain_request import SetAppDomainRequest
from paas.openapi_client.models.sources_deploy200_response import SourcesDeploy200Response
from paas.openapi_client.models.turn_app_request import TurnAppRequest
from paas.openapi_client.models.update_envs import UpdateEnvs
from paas.openapi_client.models.update_envs200_response import UpdateEnvs200Response
from paas.openapi_client.models.update_envs_variables_inner import UpdateEnvsVariablesInner

def create_sdk(token: str):
    config = paas.openapi_client.Configuration(
        host = "https://api.iran.liara.ir"
    )
    config.api_key['jwt'] = f'Bearer {token}'
    
    return paas.openapi_client.ApiClient(config)