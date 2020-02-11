using System;
using System.ComponentModel;

namespace Uml.Cs.Dll
{
    [Flags]
    public enum UmlEnum
    {
        None = 0x00,

        /// <summary>
        /// Who is General Failure and why is he reading my hard disk?
        /// </summary>
        [Description("First flag.")]
        FirstFlag = 0x01,

        [Description("Second flag.")]
        SecondFlag = 0x02,
    }
}
