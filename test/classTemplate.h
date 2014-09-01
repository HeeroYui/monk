
namespace testMonk {
	template<typename T> class ClassTemplate {
		public:
			ClassTemplate();
			~ClassTemplate();
	};
	template<typename T, class T2> class ClassTemplateMultiple {
		public:
			ClassTemplateMultiple();
			~ClassTemplateMultiple();
			testMonk::ClassTemplate<classPlop> m_essay ponterClass
	};
}
