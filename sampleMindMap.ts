import { MindMapData } from '../types/MindMap';

export const sampleMindMap: MindMapData = {
  rootNode: {
    id: 'root',
    title: 'Software Navigation',
    url: 'https://staging.zazoon.com/dashboard',
    children: [
      {
        id: 'solutions',
        title: 'SOLUTIONS',
        isExpandable: true,
        children: [
          {
            id: 'information security',
            title: 'Information Security',
            url: 'https://staging.zazoon.com/solutions/ism',
            isExpandable: true,
            children: [
              {
                id: 'is frameworks',
                title: 'Frameworks',
                url: 'https://staging.zazoon.com/solutions/ism/frameworks',
                context: 'information security',
                parentSection: 'Information Security',
                isExpandable: true,
                frameworkListing: {
                  url: 'https://staging.zazoon.com/solutions/ism/frameworks',
                  breadcrumb: ['Information Security', 'Frameworks'],
                  availableFrameworks: [
                    {
                      id: 'iso-9001-2015',
                      title: 'Qualitätsmanagement nach ISO 9001:2015',
                      url: 'https://staging.zazoon.com/solutions/ism/frameworks/iso-9001-2015',
                      hasAssessment: true,
                      assessment: {
                        id: 'iso-9001-2015-assessment',
                        title: 'ISO 9001:2015 Assessment',
                        assessmentUrl: 'https://staging.zazoon.com/solutions/ism/frameworks/iso-9001-2015/assessment',
                        graphUrl: 'https://staging.zazoon.com/solutions/statement-graph/64747952-df53-47a8-bccb-16417af5614f'
                      }
                    }
                  ]
                }
              },
              {
                id: 'is item mappings',
                title: 'Item Mappings',
                url: 'https://staging.zazoon.com/solutions/ism/item-mappings',
                context: 'information security',
                parentSection: 'Information Security',
                isExpandable: true,
                itemMappingListing: {
                  url: 'https://staging.zazoon.com/solutions/ism/item-mappings',
                  breadcrumb: ['Information Security', 'Item Mappings'],
                  availableMappings: [
                    {
                      frameworkId: 'iso-9001-2015',
                      frameworkTitle: 'Qualitätsmanagement nach ISO 9001:2015',
                      mappings: [
                        {
                          id: 'default-mapping',
                          title: 'Default Mapping',
                          status: 'empty',
                          statusMessage: 'No mappings created yet'
                        }
                      ]
                    }
                  ]
                }
              },
              {
                id: 'is solution features',
                title: 'Solution Features',
                url: 'https://staging.zazoon.com/solutions/ism/features',
                context: 'information security',
                parentSection: 'Information Security',
                isExpandable: true,
                solutionFeatureListing: {
                  url: 'https://staging.zazoon.com/solutions/ism/features',
                  breadcrumb: ['Information Security', 'Solution Features'],
                  availableFeatures: [
                    {
                      id: 'risk-management',
                      title: 'Risk Management',
                      description: 'Identify, evaluate, and prioritize risks across your enterprise. Implement robust risk mitigation strategies to protect your business operations and ensure compliance with industry standards and regulatory requirements.',
                      viewUrl: 'https://staging.zazoon.com/solutions/ism/features/risk-management',
                      riskRegistry: {
                        url: 'https://staging.zazoon.com/risks/registry',
                        breadcrumb: ['Risks', 'Risk Registry'],
                        title: 'Risk Registry',
                        description: 'View and manage all risks in the system',
                        hasListingFeature: true
                      }
                    }
                  ]
                }
              },
              {
                id: 'is template library',
                title: 'Template Library',
                url: 'https://staging.zazoon.com/solutions/ism/templates',
                context: 'information security',
                parentSection: 'Information Security',
                isExpandable: true,
                templateLibrary: {
                  url: 'https://staging.zazoon.com/solutions/ism/templates',
                  breadcrumb: ['Information Security', 'Template Library'],
                  title: 'Template Library',
                  description: 'Access and manage process templates for Information Security',
                  section: 'Process Templates'
                }
              }
            ]
          },
          {
            id: 'data protection',
            title: 'Data Protection',
            url: 'https://staging.zazoon.com/solutions/data-protection',
            isExpandable: true,
            sectionOverview: {
              url: 'https://staging.zazoon.com/solutions/data-protection',
              breadcrumb: ['Data Protection'],
              title: 'Data Protection',
              sections: [
                {
                  id: 'dp-frameworks',
                  title: 'Frameworks',
                  url: 'https://staging.zazoon.com/solutions/data-protection/frameworks'
                },
                {
                  id: 'dp-item-mappings',
                  title: 'Item Mappings',
                  url: 'https://staging.zazoon.com/solutions/data-protection/item-mappings'
                },
                {
                  id: 'dp-solution-features',
                  title: 'Solution Features',
                  url: 'https://staging.zazoon.com/solutions/data-protection/features'
                },
                {
                  id: 'dp-template-library',
                  title: 'Template Library',
                  url: 'https://staging.zazoon.com/solutions/data-protection/templates'
                }
              ]
            },
            children: [
              {
                id: 'dp frameworks',
                title: 'Frameworks',
                url: 'https://staging.zazoon.com/solutions/data-protection/frameworks',
                context: 'data protection',
                parentSection: 'Data Protection',
                isExpandable: true,
                frameworksView: {
                  url: 'https://staging.zazoon.com/solutions/data-protection/frameworks',
                  breadcrumb: ['Data Protection', 'Frameworks'],
                  title: 'Frameworks',
                  description: 'View and manage Data Protection frameworks',
                  hasAssessmentFeature: true
                }
              },
              {
                id: 'dp item mappings',
                title: 'Item Mappings',
                url: 'https://staging.zazoon.com/solutions/data-protection/item-mappings',
                context: 'data protection',
                parentSection: 'Data Protection',
                isExpandable: true,
                itemMappingsView: {
                  url: 'https://staging.zazoon.com/solutions/data-protection/item-mappings',
                  breadcrumb: ['Data Protection', 'Item Mappings'],
                  title: 'Item Mappings',
                  description: 'View and manage mappings for Data Protection frameworks',
                  defaultStatus: 'No mappings created yet'
                }
              },
              {
                id: 'dp solution features',
                title: 'Solution Features',
                url: 'https://staging.zazoon.com/solutions/data-protection/features',
                context: 'data protection',
                parentSection: 'Data Protection',
                isExpandable: true,
                dataProtectionFeaturesView: {
                  url: 'https://staging.zazoon.com/solutions/data-protection/features',
                  breadcrumb: ['Data Protection', 'Solution Features'],
                  title: 'Solution Features',
                  features: [
                    {
                      id: 'process-modelling',
                      title: 'Process Modelling',
                      description: 'Design and document organizational processes with detailed visualizations to ensure they align with business objectives. Enhance operational efficiency, facilitate compliance, and enable effective process management and improvement across your organization.',
                      viewUrl: 'https://staging.zazoon.com/processes/registry',
                      processRegistry: {
                        url: 'https://staging.zazoon.com/processes/registry',
                        breadcrumb: ['Processes', 'Process Registry'],
                        title: 'Process Registry',
                        description: 'View and manage all processes in the system',
                        hasProcessListing: true
                      }
                    },
                    {
                      id: 'risk-management',
                      title: 'Risk Management',
                      description: 'Identify, evaluate, and prioritize risks across your enterprise. Implement robust risk mitigation strategies to protect your business operations and ensure compliance with industry standards and regulatory requirements.',
                      viewUrl: 'https://staging.zazoon.com/risks/registry',
                      riskManagement: {
                        url: 'https://staging.zazoon.com/risks/registry',
                        breadcrumb: ['Risks', 'Risk Registry'],
                        title: 'Risk Registry',
                        description: 'View and manage all risks in the system',
                        hasRiskListing: true
                      }
                    },
                    {
                      id: 'dora',
                      title: 'Digital Operational Resilience Act (DORA)',
                      description: 'DORA is a EU Regulation on digital operational resilience in the financial sector (Digital Operational Resilience Act), the European Union has created a financial sector-wide regulation for cybersecurity, ICT risks and digital operational resilience. This regulation makes a significant contribution to strengthening the...',
                      viewUrl: 'https://staging.zazoon.com/solutions/data-protection/features/dora',
                      dora: {
                        url: 'https://staging.zazoon.com/solutions/data-protection/features/dora',
                        breadcrumb: ['Data Protection', 'Solution Features', 'DORA'],
                        title: 'Digital Operational Resilience Act (DORA)',
                        description: 'EU Regulation framework for digital operational resilience'
                      }
                    }
                  ]
                }
              },
              {
                id: 'dp template library',
                title: 'Template Library',
                url: 'https://staging.zazoon.com/solutions/data-protection/templates',
                context: 'data protection',
                parentSection: 'Data Protection',
                isExpandable: true,
                dpTemplateLibrary: {
                  url: 'https://staging.zazoon.com/solutions/data-protection/templates',
                  breadcrumb: ['Data Protection', 'Template Library'],
                  title: 'Template Library',
                  description: 'View and manage policy templates for Data Protection'
                }
              }
            ]
          },
          {
            id: 'business continuity',
            title: 'Business Continuity',
            url: 'https://staging.zazoon.com/solutions/bcm',
            isExpandable: true,
            children: [
              {
                id: 'bc frameworks',
                title: 'Frameworks',
                url: 'https://staging.zazoon.com/solutions/bcm/frameworks',
                context: 'business continuity',
                parentSection: 'Business Continuity',
                isExpandable: true,
                bcFrameworksView: {
                  url: 'https://staging.zazoon.com/solutions/bcm/frameworks',
                  breadcrumb: ['Business Continuity', 'Frameworks'],
                  title: 'Frameworks',
                  description: 'View and manage Business Continuity frameworks',
                  hasAssessmentFeature: true
                }
              },
              {
                id: 'bc item mappings',
                title: 'Item Mappings',
                url: 'https://staging.zazoon.com/solutions/bcm/item-mappings',
                context: 'business continuity',
                parentSection: 'Business Continuity',
                isExpandable: true,
                bcItemMappingsView: {
                  url: 'https://staging.zazoon.com/solutions/bcm/item-mappings',
                  breadcrumb: ['Business Continuity', 'Item Mappings'],
                  title: 'Item Mappings',
                  description: 'View and manage mappings for Business Continuity frameworks',
                  defaultStatus: 'No mappings created yet'
                }
              },
              {
                id: 'bc solution features',
                title: 'Solution Features',
                url: 'https://staging.zazoon.com/solutions/bcm/features',
                context: 'business continuity',
                parentSection: 'Business Continuity',
                isExpandable: true,
                bcSolutionFeaturesView: {
                  url: 'https://staging.zazoon.com/solutions/bcm/features',
                  breadcrumb: ['Business Continuity', 'Solution Features'],
                  title: 'Solution Features',
                  features: {
                    measureManagement: {
                      id: 'measure-management',
                      title: 'Measure Management',
                      description: 'Set, track, and implement important company measures in accordance with your business objectives. This module helps to facilitate continuous improvement by ensuring that objectives are met to yield qualitative business results.',
                      viewUrl: 'https://staging.zazoon.com/measures/registry',
                      measureRegistry: {
                        url: 'https://staging.zazoon.com/measures/registry',
                        breadcrumb: ['Measures', 'Measure Registry'],
                        title: 'Measure Registry',
                        description: 'View and manage all measures in the system',
                        hasListingFeature: true
                      }
                    },
                    riskManagement: {
                      id: 'risk-management',
                      title: 'Risk Management',
                      description: 'Identify, evaluate, and prioritize risks across your enterprise. Implement robust risk mitigation strategies to protect your business operations and ensure compliance with industry standards and regulatory requirements.',
                      viewUrl: 'https://staging.zazoon.com/risks/registry',
                      riskRegistry: {
                        url: 'https://staging.zazoon.com/risks/registry',
                        breadcrumb: ['Risks', 'Risk Registry'],
                        title: 'Risk Registry',
                        description: 'View and manage all risks in the system',
                        hasListingFeature: true
                      }
                    },
                    dora: {
                      id: 'dora',
                      title: 'Digital Operational Resilience Act (DORA)',
                      description: 'DORA is a EU Regulation on digital operational resilience in the financial sector (Digital Operational Resilience Act), the European Union has created a financial sector-wide regulation for cybersecurity, ICT risks and digital operational resilience. This regulation makes a significant contribution to strengthening the...',
                      viewUrl: 'https://staging.zazoon.com/solutions/bcm/features/dora'
                    }
                  }
                }
              },
              {
                id: 'bc template library',
                title: 'Template Library',
                url: 'https://staging.zazoon.com/solutions/bcm/templates',
                context: 'business continuity',
                parentSection: 'Business Continuity',
                isExpandable: true,
                bcTemplateLibraryView: {
                  url: 'https://staging.zazoon.com/solutions/bcm/templates',
                  breadcrumb: ['Business Continuity', 'Template Library'],
                  title: 'Template Library',
                  description: 'View and manage process templates for Business Continuity',
                  section: 'Process Templates'
                }
              }
            ]
          },
          {
            id: 'enterprise risk',
            title: 'Enterprise Risk',
            url: 'https://staging.zazoon.com/solutions/erm',
            isExpandable: true,
            sectionOverview: {
              url: 'https://staging.zazoon.com/solutions/erm',
              breadcrumb: ['Enterprise Risk'],
              title: 'Enterprise Risk',
              sections: [
                {
                  id: 'er-frameworks',
                  title: 'Frameworks',
                  url: 'https://staging.zazoon.com/solutions/erm/frameworks'
                },
                {
                  id: 'er-item-mappings',
                  title: 'Item Mappings',
                  url: 'https://staging.zazoon.com/solutions/erm/item-mappings'
                },
                {
                  id: 'er-solution-features',
                  title: 'Solution Features',
                  url: 'https://staging.zazoon.com/solutions/erm/features'
                },
                {
                  id: 'er-template-library',
                  title: 'Template Library',
                  url: 'https://staging.zazoon.com/solutions/erm/templates'
                }
              ]
            },
            children: [
              {
                id: 'er frameworks',
                title: 'Frameworks',
                url: 'https://staging.zazoon.com/solutions/erm/frameworks',
                context: 'enterprise risk',
                parentSection: 'Enterprise Risk',
                isExpandable: true,
                frameworksView: {
                  url: 'https://staging.zazoon.com/solutions/erm/frameworks',
                  breadcrumb: ['Enterprise Risk', 'Frameworks'],
                  title: 'Frameworks',
                  description: 'View and manage Enterprise Risk frameworks',
                  hasAssessmentFeature: true
                }
              },
              {
                id: 'er item mappings',
                title: 'Item Mappings',
                url: 'https://staging.zazoon.com/solutions/erm/item-mappings',
                context: 'enterprise risk',
                parentSection: 'Enterprise Risk',
                isExpandable: true,
                itemMappingsView: {
                  url: 'https://staging.zazoon.com/solutions/erm/item-mappings',
                  breadcrumb: ['Enterprise Risk', 'Item Mappings'],
                  title: 'Item Mappings',
                  description: 'View and manage mappings for Enterprise Risk frameworks',
                  defaultStatus: 'No mappings created yet'
                }
              },
              {
                id: 'er solution features',
                title: 'Solution Features',
                url: 'https://staging.zazoon.com/solutions/erm/features',
                context: 'enterprise risk',
                parentSection: 'Enterprise Risk',
                isExpandable: true,
                solutionFeatureListing: {
                  url: 'https://staging.zazoon.com/solutions/erm/features',
                  breadcrumb: ['Enterprise Risk', 'Solution Features'],
                  availableFeatures: [
                    {
                      id: 'audits',
                      title: 'Audits',
                      description: 'Plan, conduct, and manage audit activities to ensure thorough evaluation of processes, controls, and compliance. This module supports internal and external audits, helping to identify gaps and ensure continuous improvement.',
                      viewUrl: 'https://staging.zazoon.com/solutions/erm/features/audits'
                    },
                    {
                      id: 'control-management',
                      title: 'Control Management',
                      description: 'Develop, implement, and monitor internal controls to mitigate risks and ensure regulatory compliance. This module provides a comprehensive approach to managing controls, from design to ongoing assessment, to safeguard your business.',
                      viewUrl: 'https://staging.zazoon.com/solutions/erm/features/controls'
                    },
                    {
                      id: 'documents',
                      title: 'Documents',
                      description: 'Securely store, manage, and share essential documents within your organization. This module ensures that documents are easily accessible, compliant with retention policies, and that their integrity is maintained throughout their lifecycle.',
                      viewUrl: 'https://staging.zazoon.com/solutions/erm/features/documents'
                    },
                    {
                      id: 'guests',
                      title: 'Guests',
                      description: 'Manage and monitor the activities of visitors to your company premises. This module helps you ensure security by tracking visitor access, managing visitor data, and maintaining records to comply with internal policies and regulatory requirements.',
                      viewUrl: 'https://staging.zazoon.com/solutions/erm/features/guests'
                    },
                    {
                      id: 'incidents',
                      title: 'Incidents',
                      description: '',
                      viewUrl: 'https://staging.zazoon.com/solutions/erm/features/incidents'
                    },
                    {
                      id: 'measure-management',
                      title: 'Measure Management',
                      description: 'Set, track, and implement important company measures in accordance with your business objectives. This module helps to facilitate continuous improvement by ensuring that objectives are met to yield qualitative business results.',
                      viewUrl: 'https://staging.zazoon.com/solutions/erm/features/measures'
                    },
                    {
                      id: 'policy-management',
                      title: 'Policy Management',
                      description: 'Create, distribute, and manage organizational policies to ensure they are consistently followed. This module helps maintain compliance with regulatory requirements and internal guidelines by keeping policies up-to-date and accessible.',
                      viewUrl: 'https://staging.zazoon.com/solutions/erm/features/policies'
                    },
                    {
                      id: 'process-modelling',
                      title: 'Process Modelling',
                      description: 'Design and document organizational processes with detailed visualizations to ensure they align with business objectives. Enhance operational efficiency, facilitate compliance, and enable effective process management and improvement across your organization.',
                      viewUrl: 'https://staging.zazoon.com/solutions/erm/features/processes'
                    },
                    {
                      id: 'risk-management',
                      title: 'Risk Management',
                      description: 'Identify, evaluate, and prioritize risks across your enterprise. Implement robust risk mitigation strategies to protect your business operations and ensure compliance with industry standards and regulatory requirements.',
                      viewUrl: 'https://staging.zazoon.com/risks/registry',
                      riskRegistry: {
                        url: 'https://staging.zazoon.com/risks/registry',
                        breadcrumb: ['Risks', 'Risk Registry'],
                        title: 'Risk Registry',
                        description: 'View and manage all risks in the system',
                        hasListingFeature: true
                      }
                    },
                    {
                      id: 'framework',
                      title: 'Framework',
                      description: '',
                      viewUrl: 'https://staging.zazoon.com/solutions/erm/features/framework'
                    },
                    {
                      id: 'third-party-risks',
                      title: 'Third Party Risks',
                      description: 'Oversee and manage your organization\'s relationships with vendors and suppliers. This module allows you to track vendor contacts, contracts and certifications as well as ensure compliance with contractual obligations, and mitigate risks associated with third-party services.',
                      viewUrl: 'https://staging.zazoon.com/solutions/erm/features/third-party-risks'
                    },
                    {
                      id: 'asset-management',
                      title: 'Asset Management',
                      description: '',
                      viewUrl: 'https://staging.zazoon.com/solutions/erm/features/assets'
                    },
                    {
                      id: 'dora',
                      title: 'Digital Operational Resilience Act (DORA)',
                      description: 'DORA is a EU Regulation on digital operational resilience in the financial sector (Digital Operational Resilience Act), the European Union has created a financial sector-wide regulation for cybersecurity, ICT risks and digital operational resilience. This regulation makes a significant contribution to...',
                      viewUrl: 'https://staging.zazoon.com/solutions/erm/features/dora'
                    }
                  ]
                }
              },
              {
                id: 'er template library',
                title: 'Template Library',
                url: 'https://staging.zazoon.com/solutions/erm/templates',
                context: 'enterprise risk',
                parentSection: 'Enterprise Risk',
                isExpandable: true,
                templateLibrary: {
                  url: 'https://staging.zazoon.com/solutions/erm/templates',
                  breadcrumb: ['Enterprise Risk', 'Template Library'],
                  title: 'Template Library',
                  description: 'Access and manage process templates for Enterprise Risk',
                  section: 'Process Templates'
                }
              }
            ]
          }
        ]
      }
    ]
  }
}; 